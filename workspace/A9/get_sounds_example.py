import soundDownload as SD

Key = '7acfdabe4c53a12bc236818da60c21f2d0c19c64'

SD.downloadSoundsFreesound(queryText='bassoon', API_Key = Key, outputDir='./tmp', topNResults=20, duration=(0,3), tag='multisample')

SD.downloadSoundsFreesound(queryText='guitar', API_Key = Key, outputDir='./tmp', topNResults=20, duration=(0,3), tag='multisample')

SD.downloadSoundsFreesound(queryText='violin', API_Key = Key, outputDir='./tmp', topNResults=20, duration=(0,3), tag='multisample')