# inference.ps1 — Hook SessionStart : declenche le cycle d'inference active
# Lit les 4 organes cognitifs (MODELE, PERCEPTION, PREDICTION, ERREUR),
# enonce la prediction a voix haute, injecte le contexte complet pour Claude.
# IMPORTANT : seul le JSON final va sur stdout. Tout autre output devient input pour Claude.

$ErrorActionPreference = 'SilentlyContinue'

# --- Lecture des 4 organes ---
$modele     = ''
$perception = ''
$prediction = ''
$erreur     = ''
if (Test-Path 'MODELE.md')     { $modele     = Get-Content 'MODELE.md'     -Raw -Encoding UTF8 }
if (Test-Path 'PERCEPTION.md') { $perception = Get-Content 'PERCEPTION.md' -Raw -Encoding UTF8 }
if (Test-Path 'PREDICTION.md') { $prediction = Get-Content 'PREDICTION.md' -Raw -Encoding UTF8 }
if (Test-Path 'ERREUR.md')     { $erreur     = Get-Content 'ERREUR.md'     -Raw -Encoding UTF8 }

# --- Extraction de l'action proposee depuis PREDICTION.md ---
$action = ''
if ($prediction) {
    $lines = $prediction -split "`n"
    $capture = $false
    foreach ($line in $lines) {
        $clean = $line.Trim()
        if ($clean -match '^##\s*Action') { $capture = $true; continue }
        if ($capture -and $clean -match '^##') { break }
        if ($capture -and $clean -ne '' -and $clean -notmatch '^[#>\-\*]') {
            $action = $clean
            break
        }
    }
}

# --- TTS asynchrone (fr-CA prioritaire) ---
try {
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

    $voices = $synth.GetInstalledVoices() | Where-Object { $_.Enabled }
    $frCa  = $voices | Where-Object { $_.VoiceInfo.Culture.Name -eq 'fr-CA' } | Select-Object -First 1
    $frFr  = $voices | Where-Object { $_.VoiceInfo.Culture.Name -eq 'fr-FR' } | Select-Object -First 1
    $frAny = $voices | Where-Object { $_.VoiceInfo.Culture.Name -like 'fr-*' } | Select-Object -First 1
    $voice = if ($frCa) { $frCa } elseif ($frFr) { $frFr } else { $frAny }
    if ($voice) { $synth.SelectVoice($voice.VoiceInfo.Name) }

    $greeting = if ($action) {
        "Inference active. Je propose : $action"
    } else {
        "Cyborg en ligne."
    }
    $synth.SpeakAsync($greeting) | Out-Null
} catch {
    # TTS optionnel — l'injection de contexte reste prioritaire
}

# --- Injection du contexte cognitif complet pour Claude ---
$context = @"
[Hook Cyborg — cycle d'inference active au demarrage de session]

=== MODELE.md (modele interne, invariants, mission) ===
$modele

=== PERCEPTION.md (etat observe au temps t-1, derniere fermeture) ===
$perception

=== PREDICTION.md (inference active formulee a la derniere session) ===
$prediction

=== ERREUR.md (historique des erreurs de prediction, source d'apprentissage) ===
$erreur

=== Cycle d'inference active a executer maintenant ===
1. Comparer la PREDICTION (ce qui etait attendu) avec l'etat reel observable maintenant
2. Noter tout ecart significatif dans ERREUR.md
3. Premier message a l'humain : enoncer l'action proposee (depuis PREDICTION) et demander validation
4. A la fermeture ("fini" / "stop" / "a demain" / "on s'arrete") :
   mettre a jour PERCEPTION puis ERREUR puis (si necessaire) MODELE puis PREDICTION
5. Principe de parsimonie : ne jamais demander a l'humain de repeter le contexte.
   S'il manque, c'est qu'il n'etait pas dans les organes externalises. Donc l'ecrire maintenant.
"@

$output = @{
    hookSpecificOutput = @{
        hookEventName     = 'SessionStart'
        additionalContext = $context
    }
} | ConvertTo-Json -Depth 10 -Compress

Write-Output $output
