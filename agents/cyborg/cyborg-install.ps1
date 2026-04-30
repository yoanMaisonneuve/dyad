# cyborg-install.ps1 — Installe les 4 organes cognitifs du Cyborg dans le repertoire courant
# Usage : ouvrir PowerShell DANS le projet cible, puis :
#   powershell -ExecutionPolicy Bypass -File "C:\Users\Utilisateur\Documents\openClaude\agents\cyborg\cyborg-install.ps1"

$ErrorActionPreference = 'Stop'
$templateDir = $PSScriptRoot
$targetDir = (Get-Location).Path

Write-Host ""
Write-Host "  CYBORG  ->  $targetDir"
Write-Host ""

# --- Copie des 4 organes (ne pas ecraser si existants) ---
$created = 0
$kept    = 0
foreach ($f in @('MODELE.md', 'PERCEPTION.md', 'PREDICTION.md', 'ERREUR.md')) {
    $src = Join-Path $templateDir $f
    $dst = Join-Path $targetDir $f
    if (Test-Path $dst) {
        Write-Host "  [conserve] $f (existait deja)"
        $kept++
    } else {
        Copy-Item $src $dst
        Write-Host "  [cree]     $f"
        $created++
    }
}

# --- Creation du dossier .claude et copie du hook + settings ---
$claudeDir = Join-Path $targetDir '.claude'
if (-not (Test-Path $claudeDir)) {
    New-Item -ItemType Directory -Path $claudeDir | Out-Null
}

foreach ($f in @('settings.json', 'inference.ps1')) {
    $src = Join-Path $templateDir '.claude' | Join-Path -ChildPath $f
    $dst = Join-Path $claudeDir $f
    if (Test-Path $dst) {
        Write-Host "  [conserve] .claude/$f (existait deja)"
        $kept++
    } else {
        Copy-Item $src $dst
        Write-Host "  [cree]     .claude/$f"
        $created++
    }
}

Write-Host ""
Write-Host "  $created organe(s) cree(s), $kept conserve(s)."
Write-Host ""

# --- Confirmation vocale ---
try {
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $voices = $synth.GetInstalledVoices() | Where-Object { $_.Enabled }
    $frCa  = $voices | Where-Object { $_.VoiceInfo.Culture.Name -eq 'fr-CA' } | Select-Object -First 1
    $frFr  = $voices | Where-Object { $_.VoiceInfo.Culture.Name -eq 'fr-FR' } | Select-Object -First 1
    $frAny = $voices | Where-Object { $_.VoiceInfo.Culture.Name -like 'fr-*' } | Select-Object -First 1
    $voice = if ($frCa) { $frCa } elseif ($frFr) { $frFr } else { $frAny }
    if ($voice) { $synth.SelectVoice($voice.VoiceInfo.Name) }
    $synth.Speak("Cyborg installe. Quatre organes externalises en place. Cycle d'inference active pret.")
} catch {}

Write-Host "  Cyborg installe."
Write-Host "  Ouvre Claude Code dans ce dossier — le cycle d'inference active demarre."
Write-Host ""
