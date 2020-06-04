from src import website

web = website.WebSite("www.symbiosys.com/fr-be/")

# web.findElement("menu-item-6321")
# web.checkIfDiff()


# 1 --
# web.createReference()
# web.createComparerPicture()


## 2 -- commparaisons des images
web.findWordInPicture("beschikbaar", './public/img/controleScreenshot/www.symbiosys.com-nl-be-/23-05-2020_11-26-15.png')
