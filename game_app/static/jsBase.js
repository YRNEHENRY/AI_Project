let isWhiteMode = true;

function changeStyleMode(){
        let lienActuel = document.children[0].children[0].children[3].href
        let tabLienActuel = lienActuel.split("/")

        isWhiteMode ? (tabLienActuel[4] = 'styleDark.css') : (tabLienActuel[4] = 'styleWhite.css')
        isWhiteMode = !isWhiteMode
        document.children[0].children[0].children[3].href = tabLienActuel.join("/")
}

function startGame(){

        fetch('/game/start/').then(response => response.json()).then(function(data){
                console.log(data['state_board'])
                console.log(data['turn'])
                console.log(data['position_p1'])
                console.log(data['position_p2'])
        })
}

