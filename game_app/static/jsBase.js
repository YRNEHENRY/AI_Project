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
let players = [player_1, player_2]
let state_board
let turn

function playGame(){

        fetch('/game/isDone/').then(response => response.json()).then(async function(data){
                isDone = data['isDone']

                

                fetch('/game/play/').then(response => response.json()).then(async function(data){
                        turn = data['turn']
                        state_board = data['state_board']
                        player_1.position = data['position_p1']
                        player_2.position = data['position_p2']
                        player_1.isAi = data['player1IsAI']
                        player_2.isAi = data['player2isAI']
                        refreshGrid()
                        
                        if(!isDone){
                                if(!players[turn-1].isAi)
                                        displayPossibleMove()
                                else{
                                        url = '/game/moveAI'
                                        const reponse = await fetch(url, {
                                                method: 'POST',
                                                headers:{
                                                        'Content-Type': 'application/json',
                                                }  
                                        })
                                        .then((response) => response.json())
                                        .then((data) => {
                                        console.log('Success:', data);
                                        })
                                        .catch((error) => {
                                        console.error('Error:', error);
                                        }); 
                                        playGame() 
                                }
                        }
                        else{
                                winner = data['winner']
                                alert("Partie finie, gagnant : ", winner)
                        }
        })
        })
        
}


async function move(x, y){
        let move = [x,y]
        console.log(move)
        url = '/game/move?move=' + move
        console.log(url)
        const reponse = await fetch(url, {
                method: 'POST',
                headers:{
                        'Content-Type': 'application/json',
                },
                body: JSON.stringify(move),
        })
        .then((response) => response.json())
        .then((data) => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
        turn = turn == 1 ? 2 : 1  
        playGame()   
}

function displayPossibleMove(){
        let table = document.getElementsByClassName("grid")[0].children[0]

        let playerPosition = turn == 1 ? player_1.position : player_2.position
        let possibleMove = []

        opponentPlayer = "player" + (turn == 1 ? 2 : 1)

        if((playerPosition[0] - 1) >= 0 && table.children[playerPosition[0] - 1].children[playerPosition[1]].className != opponentPlayer)
                possibleMove.push([(playerPosition[0] - 1), playerPosition[1]])

        if((playerPosition[1] - 1 >= 0) && table.children[playerPosition[0]].children[playerPosition[1] - 1].className != opponentPlayer)
                possibleMove.push([playerPosition[0], (playerPosition[1] - 1)])

        if((playerPosition[0] + 1) <= 3 && table.children[playerPosition[0] + 1].children[playerPosition[1]].className != opponentPlayer)
                possibleMove.push([(playerPosition[0] + 1), playerPosition[1]])

        if((playerPosition[1] + 1 <= 3) && table.children[playerPosition[0]].children[playerPosition[1] + 1].className != opponentPlayer)
                possibleMove.push([playerPosition[0], (playerPosition[1] + 1)])


        for(let i in possibleMove){
                
                table.children[possibleMove[i][0]].children[possibleMove[i][1]].className += " movable"
                table.children[possibleMove[i][0]].children[possibleMove[i][1]].addEventListener("click", move.bind(null, possibleMove[i][0], possibleMove[i][1]))
                
        }
        
        
   
}


function refreshGrid(){
        let table = document.getElementsByClassName("grid")[0].children[0]

        for(let i in state_board){
                
                for(let y in state_board[i]){
                        table.children[i].children[y].replaceWith(table.children[i].children[y].cloneNode(true))
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
        table.children[player_1.position[0]].children[player_1.position[1]].innerHTML = "P1"
        table.children[player_2.position[0]].children[player_2.position[1]].innerHTML = "P2"

}
