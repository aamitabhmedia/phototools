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

Write-Host $HOME_GEOTAG.lat
Write-Host $HOME_GEOTAG.lon
Write-Host $HOME_GEOTAG.latref
Write-Host $HOME_GEOTAG.lonref
