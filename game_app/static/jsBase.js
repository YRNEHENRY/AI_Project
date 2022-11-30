let isWhiteMode = true;

function changeStyleMode(){
        let lienActuel = document.children[0].children[0].children[3].href
        let tabLienActuel = lienActuel.split("/")

        isWhiteMode ? (tabLienActuel[4] = 'styleDark.css') : (tabLienActuel[4] = 'styleWhite.css')
        isWhiteMode = !isWhiteMode
        document.children[0].children[0].children[3].href = tabLienActuel.join("/")
}

let player_1 = {icon : '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><path d="M352 124.5l-51.9-13c-6.5-1.6-11.3-7.1-12-13.8s2.8-13.1 8.7-16.1l40.8-20.4L294.4 28.8c-5.5-4.1-7.8-11.3-5.6-17.9S297.1 0 304 0H416h32 16c30.2 0 58.7 14.2 76.8 38.4l57.6 76.8c6.2 8.3 9.6 18.4 9.6 28.8c0 26.5-21.5 48-48 48H538.5c-17 0-33.3-6.7-45.3-18.7L480 160H448v21.5c0 24.8 12.8 47.9 33.8 61.1l106.6 66.6c32.1 20.1 51.6 55.2 51.6 93.1C640 462.9 590.9 512 530.2 512H496 432 32.3c-3.3 0-6.6-.4-9.6-1.4C13.5 507.8 6 501 2.4 492.1C1 488.7 .2 485.2 0 481.4c-.2-3.7 .3-7.3 1.3-10.7c2.8-9.2 9.6-16.7 18.6-20.4c3-1.2 6.2-2 9.5-2.2L433.3 412c8.3-.7 14.7-7.7 14.7-16.1c0-4.3-1.7-8.4-4.7-11.4l-44.4-44.4c-30-30-46.9-70.7-46.9-113.1V181.5v-57zM512 72.3c0-.1 0-.2 0-.3s0-.2 0-.3v.6zm-1.3 7.4L464.3 68.1c-.2 1.3-.3 2.6-.3 3.9c0 13.3 10.7 24 24 24c10.6 0 19.5-6.8 22.7-16.3zM130.9 116.5c16.3-14.5 40.4-16.2 58.5-4.1l130.6 87V227c0 32.8 8.4 64.8 24 93H112c-6.7 0-12.7-4.2-15-10.4s-.5-13.3 4.6-17.7L171 232.3 18.4 255.8c-7 1.1-13.9-2.6-16.9-9s-1.5-14.1 3.8-18.8L130.9 116.5z"/></svg> '}
let player_2 = {icon : '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M448 238.1V160h16l9.8 19.6c12.5 25.1 42.2 36.4 68.3 26c20.5-8.2 33.9-28 33.9-50.1V80c0-19.1-8.4-36.3-21.7-48H560c8.8 0 16-7.2 16-16s-7.2-16-16-16H480 448C377.3 0 320 57.3 320 128H224 203.2 148.8c-30.7 0-57.6 16.3-72.5 40.8C33.2 174.5 0 211.4 0 256v56c0 13.3 10.7 24 24 24s24-10.7 24-24V256c0-13.4 6.6-25.2 16.7-32.5c1.6 13 6.3 25.4 13.6 36.4l28.2 42.4c8.3 12.4 6.4 28.7-1.2 41.6c-16.5 28-20.6 62.2-10 93.9l17.5 52.4c4.4 13.1 16.6 21.9 30.4 21.9h33.7c21.8 0 37.3-21.4 30.4-42.1l-20.8-62.5c-2.1-6.4-.5-13.4 4.3-18.2l12.7-12.7c13.2-13.2 20.6-31.1 20.6-49.7c0-2.3-.1-4.6-.3-6.9l84 24c4.1 1.2 8.2 2.1 12.3 2.8V480c0 17.7 14.3 32 32 32h32c17.7 0 32-14.3 32-32V315.7c19.2-19.2 31.5-45.7 32-75.7h0v-1.9zM496 96c-8.8 0-16-7.2-16-16s7.2-16 16-16s16 7.2 16 16s-7.2 16-16 16z"/></svg>'}
let players = [player_1, player_2]
let state_board
let turn
let isDone = false
let movement
let idBoard
let size

function startGame(){
        fetch('/game/start/').then(response => response.json()).then(async function(data){
                turn = data['turn']
                idBoard = data['id_board']
                state_board = data['state_board']
                player_1.position = data['position_p1']
                player_2.position = data['position_p2']
                player_1.isAi = data['player1_is_AI']
                player_2.isAi = data['player2_is_AI']
                isDone = data['is_done']
                winner = data['winner']
                size = data['size']
                
                if(!isDone)
                        turnGame()
                else{
                        refreshGrid()      
                }    
        }
)}

function turnGame(){
        refreshGrid()
        displayPossibleMove()
}


function move(x, y){
        let move = [x,y]

        if (move[0] < players[turn - 1].position[0]){
                movement = "UP"
                players[turn-1].position[0] -= 1
        }
        else if (move[0] > players[turn - 1].position[0]){
                movement = "DOWN"
                players[turn-1].position[0] += 1
        }
        else if (move[1] < players[turn - 1].position[1]){
                movement = "LEFT"
                players[turn-1].position[1] -= 1
        }
        else{
                movement = "RIGHT"
                players[turn-1].position[1] += 1
        }
        updateState(movement)
        parameter = movement + "|" + idBoard + "|" + turn + "|" + state_board
        fetch("/game/move?movement=" + parameter, {
                method : "GET",
                headers : {"Content-Type": "application/json"},
                
        }).then(response => response.json()).then(async function(data){
                turn = data['turn']
                state_board = data['state_board']
                player_1.position = data['position_p1']
                player_2.position = data['position_p2']
                player_1.isAi = data['player1_is_AI']
                player_2.isAi = data['player2_is_AI']
                isDone = data['is_done'] 
                winner = data['winner']
                if(!isDone)
                        turnGame()
                else{
                        refreshGrid()         
                }
        })
        
}

function updateState(movement){



        x = players[turn - 1].position[0]
        y = players[turn - 1].position[1]
        state_board[x][y] = turn
        turn = turn == 1 ? 2 : 1    
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

        if((playerPosition[0] + 1) <=  (size - 1) && table.children[playerPosition[0] + 1].children[playerPosition[1]].className != opponentPlayer)
                possibleMove.push([(playerPosition[0] + 1), playerPosition[1]])

        if((playerPosition[1] + 1 <= (size - 1)) && table.children[playerPosition[0]].children[playerPosition[1] + 1].className != opponentPlayer)
                possibleMove.push([playerPosition[0], (playerPosition[1] + 1)])


        for(let i in possibleMove){
                
                table.children[possibleMove[i][0]].children[possibleMove[i][1]].children[0].className += "show_move"
                table.children[possibleMove[i][0]].children[possibleMove[i][1]].addEventListener("click", move.bind(null, possibleMove[i][0], possibleMove[i][1]))
                
        }
        
        
   
}


function refreshGrid(){
        let table = document.getElementsByClassName("grid")[0].children[0]
        for(let i in state_board){
                
                for(let y in state_board[i]){
                        table.children[i].children[y].replaceWith(table.children[i].children[y].cloneNode(true))
                        switch(state_board[i][y]){
                                case 0 :
                                        table.children[i].children[y].className = "neutral"
                                        break;
                                case 1 :
                                        table.children[i].children[y].className = "player1"
                                        break;
                                case 2 :
                                        table.children[i].children[y].className = "player2"
                                        break;
                        }
                        table.children[i].children[y].children[0].innerHTML = ""
                        table.children[i].children[y].children[0].className = ""
                        
                }
        }
        table.children[player_1.position[0]].children[player_1.position[1]].children[0].innerHTML = player_1.icon
        table.children[player_2.position[0]].children[player_2.position[1]].children[0].innerHTML = player_2.icon

}