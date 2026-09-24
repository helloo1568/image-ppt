param(
    [Parameter(Mandatory = $true)][string]$Deck,
    [Parameter(Mandatory = $true)][string]$OutputDir,
    [Parameter(Mandatory = $true)][int]$Width,
    [Parameter(Mandatory = $true)][int]$Height
)

$ErrorActionPreference = 'Stop'
$app = $null
$presentation = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $presentation = $app.Presentations.Open($Deck, $true, $false, $false)
    for ($index = 1; $index -le $presentation.Slides.Count; $index++) {
        $target = Join-Path $OutputDir ('{0:D3}.png' -f $index)
        $presentation.Slides.Item($index).Export($target, 'PNG', $Width, $Height)
    }
}
finally {
    if ($null -ne $presentation) {
        $presentation.Close()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($presentation)
    }
    if ($null -ne $app) {
        $app.Quit()
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($app)
    }
}
