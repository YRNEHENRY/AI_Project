let isWhiteMode = true;

function changeStyleMode(){

        let lienActuel = document.children[0].children[0].children[3].href
        let tabLienActuel = lienActuel.split("/")

        if(isWhiteMode){
            tabLienActuel[4] = 'styleDark.css'
            isWhiteMode = false
        }
        else{
            tabLienActuel[4] = 'styleWhite.css'
            isWhiteMode = true
        }
        document.children[0].children[0].children[3].href = tabLienActuel.join("/")
}