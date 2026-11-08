# Lee data/frases_control.txt y genera un WAV por frase con la voz «Microsoft Helena Desktop» (16 kHz, mono, 16 bits).
# Salida: data/generado/voz/frase_NN.wav
param([string]$Raiz = (Split-Path -Parent $PSScriptRoot))
Add-Type -AssemblyName System.Speech
$frases = Get-Content -Encoding UTF8 (Join-Path $Raiz 'data\frases_control.txt') | Where-Object { $_.Trim() -ne '' }
$dir = Join-Path $Raiz 'data\generado\voz'
New-Item -ItemType Directory -Force $dir | Out-Null
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(16000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
for ($i = 0; $i -lt $frases.Count; $i++) {
    $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $s.SelectVoice('Microsoft Helena Desktop')
    $s.Rate = 0
    $ruta = Join-Path $dir ('frase_{0:D2}.wav' -f $i)
    $s.SetOutputToWaveFile($ruta, $fmt)
    $s.Speak($frases[$i])
    $s.Dispose()
}
"{0} frases sintetizadas en {1}" -f $frases.Count, $dir
