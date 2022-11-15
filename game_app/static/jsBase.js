let isWhiteMode = true;

function changeStyleMode(){
        let lienActuel = document.children[0].children[0].children[3].href
        let tabLienActuel = lienActuel.split("/")

        isWhiteMode ? (tabLienActuel[4] = 'styleDark.css') : (tabLienActuel[4] = 'styleWhite.css')
        isWhiteMode = !isWhiteMode
        document.children[0].children[0].children[3].href = tabLienActuel.join("/")
}

let player_1 = {icon : "../Player_icon/horse.svg"}
let player_2 = {icon : "../Player_icon/spider.svg"}
let state_board
let turn

function startGame(){

        fetch('/game/start/').then(response => response.json()).then(function(data){
                turn = data['turn']
                state_board = data['state_board']
                player_1.position_p1 = data['position_p1']
                player_2.position_p2 = data['position_p2']
                refreshGrid()
        })
        
}

function refreshGrid(){
        let table = document.getElementsByClassName("grid")[0].children[0]

        for(let i in state_board){
                
                for(let y in state_board[i]){
                        switch(state_board[i][y]){
                                case 0 :table.children[i].children[y].innerHTML = ""
                                        table.children[i].children[y].className = "neutral"
                                        break;
                                case 1 : table.children[i].children[y].innerHTML = "1"
                                        table.children[i].children[y].className = "player1"
                                        break;
                                case 2 : table.children[i].children[y].innerHTML = "2"
                                        table.children[i].children[y].className = "player2"
                                        break;
                        }
                        table.children[i].children[y]
                }
        }
        table.children[player_1.position_p1[0]].children[player_1.position_p1[1]].innerHTML = "P1"
        table.children[player_2.position_p2[0]].children[player_2.position_p2[1]].innerHTML = "P2"

}

