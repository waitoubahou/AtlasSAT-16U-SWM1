param([string]$RunName="")
$ErrorActionPreference="Stop"
$study=(Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not $RunName) {$RunName=(Get-Date -Format "yyyyMMddTHHmmss")+"_"+[guid]::NewGuid().ToString("N").Substring(0,8)}
if ($RunName -notmatch '^[A-Za-z0-9_-]+$') {throw "Use letters, digits, underscore or hyphen"}
$run=[IO.Path]::GetFullPath((Join-Path $study ("working/gmat/"+$RunName)))
if(-not $run.StartsWith($study+[IO.Path]::DirectorySeparatorChar)){throw "Unsafe working directory"}
if(Test-Path -LiteralPath $run){throw "Refuse an existing run directory"}
New-Item -ItemType Directory -Path $run -Force | Out-Null
$source=Join-Path $study "simulation/GMAT/AtlasSAT_Nominal_30days_GUI.script"
$text=[IO.File]::ReadAllText($source)
foreach($pair in @(@("AtlasStates","AtlasSAT_GUI_Nominal_30days_states.txt"),@("AtlasOEM","AtlasSAT_GUI_Nominal_30days.oem"))){
 $file=(Join-Path $run $pair[1]).Replace("\","/")
 $pattern="(GMAT "+$pair[0]+"\.Filename = )'[^']+'"
 if([regex]::Matches($text,$pattern).Count -ne 1){throw "Expected exactly one output filename per subscriber"}
 $text=[regex]::Replace($text,$pattern,('$1'+ "'"+$file+"'"))
}
$mission=Join-Path $run "AtlasSAT_Nominal_30days_GUI.script"
[IO.File]::WriteAllText($mission,$text,(New-Object Text.UTF8Encoding($false)))
Write-Output "Open this fresh script using GMAT File > Open:"
Write-Output $mission
Write-Output "Only two output filenames changed. GMAT has NOT been launched or executed."
