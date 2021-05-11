# -------------------------------------------------------
# Fix-Pfilm
# -------------------------------------------------------
function Fix-Pfilm {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="PFilm Album Folder")]
        [string]$Folder,

        [Parameter(Mandatory=$false,
                    HelpMessage="Caption: Update caption in the images")]
        [switch]$c=$false,

        [Parameter(Mandatory=$false,
                HelpMessage="Force album name to caption of all images")]
        [switch]$f=$false,

        [Parameter(Mandatory=$false,
                HelpMessage="Rename the images")]
        [switch]$r=$false,

        [Parameter(Mandatory=$false,
                HelpMessage="Test only: Do not execute exiftool")]
        [switch]$t=$false,

        [Parameter(Mandatory=$false,
                HelpMessage="Verbose")]
        [switch]$v=$false
    )

    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta
    Write-Host "$($Folder)" -ForegroundColor Magenta
    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "Caption    = $c" -ForegroundColor Yellow
    Write-Host "Force      = $f" -ForegroundColor Yellow
    Write-Host "Rename     = $r" -ForegroundColor Yellow
    Write-Host "Test Only  = $t" -ForegroundColor Yellow

    # Remove the trailing slash
    $Folder = $Folder.trim('\')
}