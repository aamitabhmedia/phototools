function Get-FolderAbbrev {

    # [CmdletBinding()]
    # param(
    #     [Parameter(Mandatory)]
    #     [string]$AlbumName
    # )

    # $splits = $AlbumName.Split(" ")
    # $albumDate = $splits[0]
    # $albumDesc = $splits[1..($splits.Count-1)]

    # $datesplits = $splits.Split('-')
    # if ($datesplits.Count -lt 3) {
    #     Write-Host "ERROR: Bad DATE format $($AlbumName)"
    #     return $null
    # }
    # $album_year = $datesplits[0]
    # if ($album_year.length -lt 4) {
    #     Write-Host "ERROR: Bad YEAR format $($AlbumName)"
    #     return $null
    # }
    # $album_year_2digit = $album_year.Substring(2,2)
    # $album_month = $datesplits[1]
    # if ($album_month.length -lt 2) {
    #     Write-Host "ERROR: Bad MONTH format $($AlbumName)"
    #     return $null
    # }
    # $album_day = $datesplits[2]
    # if ($album_day.length -lt 4) {
    #     Write-Host "ERROR: Bad DAY format $($AlbumName)"
    #     return $null
    # }

    # $abbrev = $null
    # foreach ($word in $albumDesc) {
    #     $word = (Get-Culture).TextInfo.ToTitleCase($word)
    #     $wordabrv = $word.Substring(0,3)
    #     $abbrev += $wordabrv
    # }

    # return $abbrev
}