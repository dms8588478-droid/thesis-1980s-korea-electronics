$ErrorActionPreference = "Stop"
$sc = $PSScriptRoot
$outDir = "C:\Users\user\OneDrive\바탕 화면\1980년대 전자공업"
if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Force $outDir | Out-Null }
$out = Join-Path $outDir "261000 최낙은 발표문 _new.hwp"

$hwp = New-Object -ComObject HWPFrame.HwpObject
try { $hwp.SetMessageBoxMode(0x00020000) | Out-Null } catch {}
try { $hwp.XHwpWindows.Item(0).Visible = $false } catch {}
$hwp.XHwpDocuments.Add($false) | Out-Null

function Ins($txt) {
  if ([string]::IsNullOrEmpty($txt)) { return }
  $a = $hwp.CreateAction("InsertText"); $s = $a.CreateSet(); $a.GetDefault($s)
  $s.SetItem("Text", $txt) | Out-Null; $a.Execute($s) | Out-Null
}
function SetChar($size, $bold) {
  $a = $hwp.CreateAction("CharShape"); $s = $a.CreateSet(); $a.GetDefault($s)
  $s.SetItem("Height", [int]($size * 100)) | Out-Null
  $s.SetItem("Bold", [int]$bold) | Out-Null
  foreach ($k in @("Hangul","Latin","Hanja","Japanese","Other","Symbol","User")) {
    try { $s.SetItem("FaceName" + $k, "함초롬바탕") | Out-Null } catch {}
  }
  $a.Execute($s) | Out-Null
}

$lines = [System.IO.File]::ReadAllLines((Join-Path $sc "ops.txt"), [System.Text.Encoding]::UTF8)
$n = 0
foreach ($ln in $lines) {
  $n++
  $ix = $ln.IndexOf("`t")
  if ($ix -lt 0) { $op = $ln; $arg = "" } else { $op = $ln.Substring(0, $ix); $arg = $ln.Substring($ix + 1) }
  switch ($op) {
    "H1" { SetChar 14 1; Ins $arg; $hwp.HAction.Run("BreakPara") | Out-Null; SetChar 10 0 }
    "H2" { SetChar 12 1; Ins $arg; $hwp.HAction.Run("BreakPara") | Out-Null; SetChar 10 0 }
    "H3" { SetChar 11 1; Ins $arg; $hwp.HAction.Run("BreakPara") | Out-Null; SetChar 10 0 }
    "S"  { Ins $arg }
    "F"  {
      $hwp.HAction.Run("InsertFootnote") | Out-Null
      SetChar 9 0
      Ins $arg
      $hwp.HAction.Run("CloseEx") | Out-Null
      SetChar 10 0
    }
    "P"  { $hwp.HAction.Run("BreakPara") | Out-Null }
    "TB" {
      $p = $arg.Split(" ")
      $a = $hwp.CreateAction("TableCreate"); $s = $a.CreateSet(); $a.GetDefault($s)
      $s.SetItem("Rows", [int]$p[0]) | Out-Null; $s.SetItem("Cols", [int]$p[1]) | Out-Null
      $s.SetItem("WidthType", 2) | Out-Null; $s.SetItem("HeightType", 1) | Out-Null
      $a.Execute($s) | Out-Null
      $script:firstCell = $true
    }
    "TC" {
      if (-not $script:firstCell) { $hwp.HAction.Run("TableRightCell") | Out-Null }
      $script:firstCell = $false
      SetChar 9 0
      Ins $arg
    }
    "TE" { $hwp.HAction.Run("MoveDocEnd") | Out-Null; SetChar 10 0; $hwp.HAction.Run("BreakPara") | Out-Null }
  }
}
$hwp.SaveAs($out, "HWP", "") | Out-Null
$hwp.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($hwp) | Out-Null
[GC]::Collect(); [GC]::WaitForPendingFinalizers()
Write-Output ("ops=" + $n + " saved=" + $out)
