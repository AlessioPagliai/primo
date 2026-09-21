# Knee-flexion table across round-4 (locked-knee reference) and all round-5 variants.
$rows = @(
  @('R4','PendBase','r4_pendbase'),
  @('R5','ArmsFwd','r5_armsfwd'), @('R5','KneeSoft','r5_kneesoft'), @('R5','KneeHard','r5_kneehard'),
  @('R5','Crouch','r5_crouch'), @('R5','KneeDefault','r5_kneedefault'), @('R5','KneeTorque','r5_kneetorque')
)
foreach ($r in $rows) {
    $pre = $r[0]; $name = $r[1]; $exp = $r[2]
    $dir = "C:\Users\WKS\isaac\IsaacLab\logs\rsl_rl\$exp"
    if (-not (Test-Path $dir)) { Write-Output "$name : no logs"; continue }
    $run = Get-ChildItem $dir -Directory | Sort-Object Name | Select-Object -Last 1
    $ck = Join-Path $run.FullName "model_2999.pt"
    if (-not (Test-Path $ck)) { Write-Output "$name : no model_2999"; continue }
    $log = "C:\Users\WKS\Documents\humanoid\rl_full_isaac\training_runs\probe_$name.log"
    cmd /c "set OMNI_KIT_ACCEPT_EULA=YES&& set OMNI_CRASHREPORTER_ENABLED=0&& set PYTHONUNBUFFERED=1&& call C:\Users\WKS\isaac\env_isaaclab\Scripts\activate.bat && cd /d C:\Users\WKS\isaac\IsaacLab && call C:\Users\WKS\isaac\IsaacLab\isaaclab.bat -p C:\Users\WKS\Documents\humanoid\rl_full_isaac\scripts\knee_probe.py --task Isaac-Velocity-$pre-$name-Play-v0 --checkpoint $ck --headless > $log 2>&1"
    $out = Select-String -Path $log -Pattern '\[KNEE\]' | ForEach-Object { $_.Line.Trim() -replace '\[KNEE\] ','' }
    if ($out) { Write-Output "=== $name"; $out | ForEach-Object { Write-Output "    $_" } }
    else { Write-Output "$name : probe failed" }
}
Write-Output "PROBE ALL DONE"
