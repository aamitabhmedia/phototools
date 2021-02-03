function Get-FolderAbbrev {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$AlbumName
    )

    $splits = $AlbumName.Split(" ")
    $albumDate = $splits[0]
    $albumDesc = $splits[1..($splits.Count-1)]

    $datesplits = $splits.Split('-')
    if ($datesplits.Count -lt 3) {
        Write-Host "ERROR: Bad DATE format $($AlbumName)"
        return $null
    }
    $album_year = $datesplits[0]
    if ($album_year.length -lt 4) {
        Write-Host "ERROR: Bad YEAR format $($AlbumName)"
        return $null
    }
    $album_year_2digit = $album_year.Substring(2,2)
    $album_month = $datesplits[1]
    if ($album_month.length -lt 2) {
        Write-Host "ERROR: Bad MONTH format $($AlbumName)"
        return $null
    }
    $album_day = $datesplits[2]
    if ($album_day.length -lt 4) {
        Write-Host "ERROR: Bad DAY format $($AlbumName)"
        return $null
    }

    $abbrev = $null
    foreach ($word in $albumDesc) {
        $word = (Get-Culture).TextInfo.ToTitleCase($word)
        $wordabrv = $word.Substring(0,3)
        $abbrev += $wordabrv
    }

    return $abbrev
}

# function fix-folder {

    # [CmdletBinding()]
    # param(
    #     [Parameter(Mandatory)]
    #     [string]$Folder,

    #     [Parameter(Mandatory)]
    #     [string]$Caption,

    #     [Parameter(Mandatory=$false)]
    #     [string]$Acronym
    # )

    # $abbrev = Get-FolderAbbrev "2013-01-20 Nani's 70th Birthday"
    # Write-Host $abbrev
    # exit

    # try {
    #     exiftool.exe "-Description=$Caption" "-Title=$Caption" "-Subject=$Caption" `
    #         "-Exif:ImageDescription=$Caption" "-iptc:ObjectName=$Caption" `
    #         "-iptc:Caption-Abstract=$Caption" -overwrite_original $Files
    # } catch {
    #     Write-Host "Error: Writing Caption"
    # }

    # $FileNamePattern = '-filename<${datetimeoriginal}_' + $Acronym + '%-c.%le'
    # Write-Host "FileNamePattern = $FileNamePattern" -ForegroundColor Yellow
    # exiftool '$FileNamePattern' -d '%Y%m%d_%H%M%S' -fileorder datetimeoriginal -overwrite_original $Files
# }

Get-FolderAbbrev("2013-01-20 Nani's 70th Birthday")
# fix-folder "P:\pics\2013\2013-01-20 Nani's 70th Birthday\test" "2013-01-20 Nani's 70th Birthday" "*D800.NEF" "Na70thBd"
