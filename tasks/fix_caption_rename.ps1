function Get-CameraModelAbbrev {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Model
    )

    $abbrevs = @{
        "Nikon D800" = "D800"
        "Nikon D70" = "D70"
    }

    $abbrev = $abbrevs[$Model]
    if ($null -eq $abbrev) {
        $abbrev = "MISSING"
    }

    return $abbrev
}

function Get-CameraModelExportFileName {
    return "exif_cam_model.csv"
}

function Get-CameraModelExportFilePath {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    $filename = Get-CameraModelExportFileName
    return Join-Path -Path $Folder -ChildPath $filename
}

function Export-FolderCameraModels {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    $outfile = Get-CameraModelExportFilePath $Folder
    exiftool -csv -Model $Folder -ext jpg -ext nef -ext cr2 -ext png -ext mov -ext mp4 -ext avi> $outfile
}

function Import-FolderCameraModels {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    $outfile = Get-CameraModelExportFilePath $Folder
    return Import-Csv $outfile
}

function Get-FolderCameraModels {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    # Export-FolderCameraModels $Folder
    $csvresult = Import-FolderCameraModels $Folder

    $modelary = @()
    $csvresult | ForEach-Object {
        $abbrev = $null
        $SourceFile = $_.SourceFile
        $model = $_.Model
        if ($null -eq $model -or "" -eq $model) {
            $abbrev = "OTHER"
        } else {
            $abbrev = Get-CameraModelAbbrev $model
        }
        $entry = [pscustomobject]@{FilePath=$SourceFile;Model=$abbrev}
        $modelary += $entry
        # $modelary.Add(@{FilePath=$SourceFile;Model=$abbrev})
        # Write-Host "'$($model)', '$($abbrev)': '$($SourceFile)'"
    }

    return $modelary

    # foreach ($cammodel in $csvresult) {
    #     model = $cammodel.Model
    #     Write-Host "model = $model" -ForegroundColor Red
    # }

    # Write-Host $csvresult

    return

    ForEach($file in $files) {
        $retval = exiftool -Model $file
        Write-Host "retval = $retval" -ForegroundColor Green
        if ($null -ne $retval) {
            $retval = Get-CameraModelAbbrev $retval
        } else {
            $retval = "OTHER"
        }

        $imagemodels.Add($file, $retval)
        # Write-Host "'$($retval)': '$($file.FullName)'" -ForegroundColor Green
    }

    return $imagemodels
}

function Get-FolderCameraModels_Incomplete {
    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$Folder
    )

    $files = Get-ChildItem $Folder\* -Include *.jpg, *.nef, *.cr2, *.png, *.mov, *.mp4, *.avi

    $imagemodels = @{}

    ForEach($file in $files) {
        $retval = exiftool -Model $file
        Write-Host "retval = $retval" -ForegroundColor Green
        if ($null -ne $retval) {
            $retval = Get-CameraModelAbbrev $retval
        } else {
            $retval = "OTHER"
        }

        $imagemodels.Add($file, $retval)
        # Write-Host "'$($retval)': '$($file.FullName)'" -ForegroundColor Green
    }

    return $imagemodels
}

function Get-FolderAbbrev {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$AlbumName
    )

    $splits = $AlbumName.Split(" ")
    $albumDate = $splits[0]
    $albumDesc = $splits[1..($splits.Count-1)]

    $datesplits = $albumDate.Split('-')
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
    if ($album_day.length -lt 2) {
        Write-Host "ERROR: Bad DAY format $($AlbumName)"
        return $null
    }

    $abbrev = $null
    foreach ($word in $albumDesc) {
        $word = (Get-Culture).TextInfo.ToTitleCase($word)
        $wordabrv = $word.Substring(0,3)
        $abbrev += $wordabrv
    }

    $abbrev += $album_year_2digit

    return $abbrev
}

function Get-FolderCaption {

    [CmdletBinding()]
    Param(
        [Parameter(Mandatory)]
        [string]$AlbumName
    )

    $splits = $AlbumName.Split(" ")
    $albumDate = $splits[0]

    $datesplits = $albumDate.Split('-')
    if ($datesplits.Count -lt 3) {
        Write-Host "ERROR: Bad DATE format $($AlbumName)"
        return $null
    }
    $album_year = $datesplits[0]
    if ($album_year.length -lt 4) {
        Write-Host "ERROR: Bad YEAR format $($AlbumName)"
        return $null
    }
    $album_month = $datesplits[1]
    if ($album_month.length -lt 2) {
        Write-Host "ERROR: Bad MONTH format $($AlbumName)"
        return $null
    }
    $album_day = $datesplits[2]
    if ($album_day.length -lt 2) {
        Write-Host "ERROR: Bad DAY format $($AlbumName)"
        return $null
    }

    $abbrev = $null

    $albumDesc = $AlbumName.Substring(11)
    Write-Host "albumDesc = $albumDesc"

    $caption = $album_year + ' ' + $albumDesc

    return $caption
}

function Fix-Folder {

    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true,
                    HelpMessage="Album Folder")]
        [string]$Folder,

        [Parameter(Mandatory=$false,
                    HelpMessage="No Caption: DO not add caption to the images")]
         [switch]$nc=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="No Rename: Do not rename the files")]
         [switch]$nr=$false,

         [Parameter(Mandatory=$false,
                    HelpMessage="Test only: Do not execute exiftool")]
         [switch]$t=$false
    )

    Write-Host "Folder     = $Folder" -ForegroundColor Yellow
    Write-Host "No Caption = $nc" -ForegroundColor Yellow
    Write-Host "No Rename  = $nr" -ForegroundColor Yellow
    Write-Host "Test Only  = $t" -ForegroundColor Yellow

    $Files = Join-Path -Path $Folder -ChildPath "*"
    
    # Get album name from folder path
    $albumName = Split-Path $Folder -Leaf

    # derive caption and abbreviation from the album folder name
    $abbrev = Get-FolderAbbrev $albumName
    $Caption = Get-FolderCaption $albumName
    Write-Host "abbrev = $abbrev"
    Write-Host "caption = $Caption"

    if (not $nc) {
        try {
            exiftool.exe "-Description=$Caption" "-Title=$Caption" "-Subject=$Caption" `
                "-Exif:ImageDescription=$Caption" "-iptc:ObjectName=$Caption" `
                "-iptc:Caption-Abstract=$Caption" -overwrite_original $Files
        } catch [Exception] {
            Write-Host "Error: Writing some Caption"
            Write-Host $_.Exception
        }
    }

    if (not $nr) {
        exiftool -ext jpg -ext nef -ext cr2 "-filename<`${datetimeoriginal}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder datetimeoriginal -overwrite_original $Files
        exiftool -ext png "-filename<`${XMP:DateCreated}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder XMP:DateCreated -overwrite_original $Files
        exiftool -ext mov "-filename<`${QuickTime:CreateDate}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder QuickTime:CreateDate -overwrite_original $Files
        exiftool -ext mp4 "-filename<`${Xmp:CreateDate}_$($abbrev)%-c.%le" -d '%Y%m%d_%H%M%S' -fileorder Xmp:CreateDate -overwrite_original $Files
    }
}

Get-FolderCameraModels "C:\Users\ajmq\Downloads\exiftest\2040\2020-01-03 Mix of all Media Types"
# Fix-Folder $args[0]
# Fix-Folder "P:\pics\2013\2013-01-20 Nani's 70th Birthday\test"
