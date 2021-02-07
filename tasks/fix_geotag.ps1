class GEOTAG
{
    [string]$lat
    [string]$lon
    [string]$latref
    [string]$lonref

    GEOTAG ([string]$lat, [string]$lon, [string]$latref, [string]$lonref)
    {
        $this.lat = $lat
        $this.lon = $lon
        $this.latref = $latref
        $this.lonref = $lonref
    }
}

$HOME_GEOTAG = [GEOTAG]::New("37.650658", "-121.870626", "N", "W")
$DELHI_GEOTAG = [GEOTAG]::New("28.533837", "77.150540", "N", "E")

# -------------------------------------------------------
# Fix-FolderGeotag
# -------------------------------------------------------
function Fix-FolderGeotagToHome {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder
    )

    Fix-FolderGeotag -Folder $Folder `
        -lat $HOME_GEOTAG.lat `
        -lon $HOME_GEOTAG.lon `
        -latref $HOME_GEOTAG.latref `
        -lonref $HOME_GEOTAG.lonref `
        -t $
}

# -------------------------------------------------------
# Fix-FolderGeotag
# -------------------------------------------------------
function Fix-FolderGeotag {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder,

        [Parameter(Mandatory=$true,
                    HelpMessage="Latitude to set")]
        [string]$lat,

        [Parameter(Mandatory=$true,
                    HelpMessage="Longitude to set")]
        [string]$lon,

        [Parameter(Mandatory=$true,
                    HelpMessage="Latitude ref value N|S")]
        [string]$latref,

        [Parameter(Mandatory=$true,
                    HelpMessage="Longitude ref value E|W")]
        [string]$lonref
    )

    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta
    Write-Host "$($Folder)" -ForegroundColor Magenta
    Write-Host "-------------------------------------------------------------------" -ForegroundColor Magenta

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "Lat        = $lat" -ForegroundColor Yellow
    Write-Host "Lon        = $lon" -ForegroundColor Yellow
    Write-Host "Latref     = $latref" -ForegroundColor Yellow
    Write-Host "Lonref     = $lonref" -ForegroundColor Yellow

    # Remove the trailing slash
    $Folder = $Folder.trim('\')

    # $Files = Join-Path -Path $Folder -ChildPath "*"
    
    exiftool "-GPSLatitude=$lat" "-GPSLongitude=$lon" "-GPSLatitudeRef=$latref" "-GPSLongitudeRef=$lonref" $Folder
}

# -------------------------------------------------------
# Fix-FolderTreeGeotag
# -------------------------------------------------------
function Fix-FolderTreeGeotag {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder,

        [Parameter(Mandatory=$true,
                    HelpMessage="Latitude to set")]
        [string]$lat,

        [Parameter(Mandatory=$true,
                    HelpMessage="Longitude to set")]
        [string]$lon,

        [Parameter(Mandatory=$true,
                    HelpMessage="Latitude ref value N|S")]
        [string]$latref,

        [Parameter(Mandatory=$true,
                    HelpMessage="Longitude ref value E|W")]
        [string]$lonref

    )

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "Lat        = $lat" -ForegroundColor Yellow
    Write-Host "Lon        = $lon" -ForegroundColor Yellow
    Write-Host "Latref     = $latref" -ForegroundColor Yellow
    Write-Host "Lonref     = $lonref" -ForegroundColor Yellow

    $dirs = Get-ChildItem -Directory $Folder
    
    foreach ($dir in $dirs) {
        Fix-FolderGeotag $dir.FullName -c:$c -r:$r -t:$t
    }
}

# -------------------------------------------------------
# Testing
# -------------------------------------------------------
# Fix-FolderGeotag "P:\pics\2040\2007-01-01 Mix Album with Big Name" 
# Fix-FolderTreeGeotag "P:\pics\2040\"
# Fix-FolderGeotag "P:\pics\2012\2012-02-14 Valentine's Day"