function fix-folder {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Files,

        [Parameter(Mandatory)]
        [string]$Caption,

        [Parameter(Mandatory=$false)]
        [string]$Acronym
    )

    try {
        exiftool.exe "-Description=$Caption" "-Title=$Caption" "-Subject=$Caption" `
            "-Exif:ImageDescription=$Caption" "-iptc:ObjectName=$Caption" `
            "-iptc:Caption-Abstract=$Caption" -overwrite_original $Files
    } catch {
        Write-Host "Error: Writing Caption"
    }

    $FileNamePattern = '-filename<${datetimeoriginal}_' + $Acronym + '%-c.%le'
    Write-Host "FileNamePattern = $FileNamePattern" -ForegroundColor Yellow
    exiftool '$FileNamePattern' -d '%Y%m%d_%H%M%S' -fileorder datetimeoriginal -overwrite_original $Files
}

# fix-folder "P:\pics\2013\2013-01-20 Nani's 70th Birthday\test" "2013-01-20 Nani's 70th Birthday" "*D800.NEF" "Na70thBd"
