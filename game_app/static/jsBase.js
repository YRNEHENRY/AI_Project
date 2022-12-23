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

function startGame(url){
        document.getElementsByClassName("grid")[0].hidden = false
        document.getElementsByClassName("score_board")[0].hidden = false
        for (let button of document.getElementsByClassName("button")){
                button.hidden = true
        }
        fetch(url).then(response => response.json()).then(async function(data){
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
                document.getElementById("player1").innerHTML = data[''];
                document.getElementById("player2").innerHTML = data[''];
                
                if(!isDone)
                        turnGame();
                else{
                        refreshGrid();
                }    
        }
)}

function turnGame(){
        refreshGrid()
        displayPossibleMove()
}


async function move(x, y){
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

        url = '/game/move/'

        const reponse = await fetch(url, {
                method: 'POST',
                headers:{
                        'Content-Type': 'application/json',
                },
                body: JSON.stringify({move : movement,idBoard: idBoard,turn: turn, state_board : state_board}),
        })
        .then((response) => response.json())
        .then((data) => {       
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
                        document.getElementById("winner").innerHTML = "Winner : " + winner;
                        refreshGrid()         
                }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
        
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

function train(){
        fetch('/train/ai/').then(response => response.json()).then(async function(data){
                alert("Fin du training")
        })
}

let settings = {
        size : {
                4: 4,
                5: 5,
                6: 6,
                7: 7,
                8: 8
        },
        colors: {
                green: "#76bb60",
                red:  "#ff6961",
                purple: "#c3b1e2",
                yellow: "#fdf698",
                blue: "#a7ecf2"
        },
        tokens: {
                cat: `<svg class="token_svg cat_svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"> <path d="M288 192h17.1c22.1 38.3 63.5 64 110.9 64c11 0 21.8-1.4 32-4v4 32V480c0 17.7-14.3 32-32 32s-32-14.3-32-32V339.2L248 448h56c17.7 0 32 14.3 32 32s-14.3 32-32 32H160c-53 0-96-43-96-96V192.5c0-16.1-12-29.8-28-31.8l-7.9-1C10.5 157.6-1.9 141.6 .2 124s18.2-30 35.7-27.8l7.9 1c48 6 84.1 46.8 84.1 95.3v85.3c34.4-51.7 93.2-85.8 160-85.8zm160 26.5v0c-10 3.5-20.8 5.5-32 5.5c-28.4 0-54-12.4-71.6-32h0c-3.7-4.1-7-8.5-9.9-13.2C325.3 164 320 146.6 320 128v0V32 12 10.7C320 4.8 324.7 .1 330.6 0h.2c3.3 0 6.4 1.6 8.4 4.2l0 .1L352 21.3l27.2 36.3L384 64h64l4.8-6.4L480 21.3 492.8 4.3l0-.1c2-2.6 5.1-4.2 8.4-4.2h.2C507.3 .1 512 4.8 512 10.7V12 32v96c0 17.3-4.6 33.6-12.6 47.6c-11.3 19.8-29.6 35.2-51.4 42.9zM400 128c0-8.8-7.2-16-16-16s-16 7.2-16 16s7.2 16 16 16s16-7.2 16-16zm48 16c8.8 0 16-7.2 16-16s-7.2-16-16-16s-16 7.2-16 16s7.2 16 16 16z"/></svg>`,
                dog: `<svg class="token_svg dog_svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M309.6 158.5L332.7 19.8C334.6 8.4 344.5 0 356.1 0c7.5 0 14.5 3.5 19 9.5L392 32h52.1c12.7 0 24.9 5.1 33.9 14.1L496 64h56c13.3 0 24 10.7 24 24v24c0 44.2-35.8 80-80 80H464 448 426.7l-5.1 30.5-112-64zM416 256.1L416 480c0 17.7-14.3 32-32 32H352c-17.7 0-32-14.3-32-32V364.8c-24 12.3-51.2 19.2-80 19.2s-56-6.9-80-19.2V480c0 17.7-14.3 32-32 32H96c-17.7 0-32-14.3-32-32V249.8c-28.8-10.9-51.4-35.3-59.2-66.5L1 167.8c-4.3-17.1 6.1-34.5 23.3-38.8s34.5 6.1 38.8 23.3l3.9 15.5C70.5 182 83.3 192 98 192h30 16H303.8L416 256.1zM464 80c0-8.8-7.2-16-16-16s-16 7.2-16 16s7.2 16 16 16s16-7.2 16-16z"/></svg>`,
                dragon: `<svg class="token_svg dragon_svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><path d="M352 124.5l-51.9-13c-6.5-1.6-11.3-7.1-12-13.8s2.8-13.1 8.7-16.1l40.8-20.4L294.4 28.8c-5.5-4.1-7.8-11.3-5.6-17.9S297.1 0 304 0H416h32 16c30.2 0 58.7 14.2 76.8 38.4l57.6 76.8c6.2 8.3 9.6 18.4 9.6 28.8c0 26.5-21.5 48-48 48H538.5c-17 0-33.3-6.7-45.3-18.7L480 160H448v21.5c0 24.8 12.8 47.9 33.8 61.1l106.6 66.6c32.1 20.1 51.6 55.2 51.6 93.1C640 462.9 590.9 512 530.2 512H496 432 32.3c-3.3 0-6.6-.4-9.6-1.4C13.5 507.8 6 501 2.4 492.1C1 488.7 .2 485.2 0 481.4c-.2-3.7 .3-7.3 1.3-10.7c2.8-9.2 9.6-16.7 18.6-20.4c3-1.2 6.2-2 9.5-2.2L433.3 412c8.3-.7 14.7-7.7 14.7-16.1c0-4.3-1.7-8.4-4.7-11.4l-44.4-44.4c-30-30-46.9-70.7-46.9-113.1V181.5v-57zM512 72.3c0-.1 0-.2 0-.3s0-.2 0-.3v.6zm-1.3 7.4L464.3 68.1c-.2 1.3-.3 2.6-.3 3.9c0 13.3 10.7 24 24 24c10.6 0 19.5-6.8 22.7-16.3zM130.9 116.5c16.3-14.5 40.4-16.2 58.5-4.1l130.6 87V227c0 32.8 8.4 64.8 24 93H112c-6.7 0-12.7-4.2-15-10.4s-.5-13.3 4.6-17.7L171 232.3 18.4 255.8c-7 1.1-13.9-2.6-16.9-9s-1.5-14.1 3.8-18.8L130.9 116.5z"/></svg>`,
                frog: `<svg class="token_svg frog_svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M368 32c41.7 0 75.9 31.8 79.7 72.5l85.6 26.3c25.4 7.8 42.8 31.3 42.8 57.9c0 21.8-11.7 41.9-30.7 52.7L400.8 323.5 493.3 416H544c17.7 0 32 14.3 32 32s-14.3 32-32 32H480c-8.5 0-16.6-3.4-22.6-9.4L346.9 360.2c11.7-36 3.2-77.1-25.4-105.7c-40.6-40.6-106.3-40.6-146.9-.1L101 324.4c-6.4 6.1-6.7 16.2-.6 22.6s16.2 6.6 22.6 .6l73.8-70.2 .1-.1 .1-.1c3.5-3.5 7.3-6.6 11.3-9.2c27.9-18.5 65.9-15.4 90.5 9.2c24.7 24.7 27.7 62.9 9 90.9c-2.6 3.8-5.6 7.5-9 10.9L261.8 416H352c17.7 0 32 14.3 32 32s-14.3 32-32 32H64c-35.3 0-64-28.7-64-64C0 249.6 127 112.9 289.3 97.5C296.2 60.2 328.8 32 368 32zm0 104c13.3 0 24-10.7 24-24s-10.7-24-24-24s-24 10.7-24 24s10.7 24 24 24z"/></svg>`,
                spider: `<svg class="token_svg spider_svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><path d="M190.4 32.6c4.8-12.4-1.4-26.3-13.8-31s-26.3 1.4-31 13.8L113.1 100c-7.9 20.7-3 44.1 12.7 59.7l57.4 57.4-80.4-26.8c-2.4-.8-4.3-2.7-5.1-5.1L78.8 128.4C74.6 115.8 61 109 48.4 113.2S29 131 33.2 143.6l18.9 56.8c5.6 16.7 18.7 29.8 35.4 35.4L148.1 256 87.6 276.2c-16.7 5.6-29.8 18.7-35.4 35.4L33.2 368.4C29 381 35.8 394.6 48.4 398.8s26.2-2.6 30.4-15.2l18.9-56.8c.8-2.4 2.7-4.3 5.1-5.1l80.4-26.8-57.4 57.4c-15.6 15.6-20.6 39-12.7 59.7l32.5 84.6c4.8 12.4 18.6 18.5 31 13.8s18.5-18.6 13.8-31l-32.5-84.6c-1.1-3-.4-6.3 1.8-8.5L192 353.9c1 52.1 43.6 94.1 96 94.1s95-41.9 96-94.1l32.3 32.3c2.2 2.2 2.9 5.6 1.8 8.5l-32.5 84.6c-4.8 12.4 1.4 26.3 13.8 31s26.3-1.4 31-13.8L462.9 412c7.9-20.7 3-44.1-12.7-59.7l-57.4-57.4 80.4 26.8c2.4 .8 4.3 2.7 5.1 5.1l18.9 56.8c4.2 12.6 17.8 19.4 30.4 15.2s19.4-17.8 15.2-30.4l-18.9-56.8c-5.6-16.7-18.7-29.8-35.4-35.4L427.9 256l60.5-20.2c16.7-5.6 29.8-18.7 35.4-35.4l18.9-56.8c4.2-12.6-2.6-26.2-15.2-30.4s-26.2 2.6-30.4 15.2l-18.9 56.8c-.8 2.4-2.7 4.3-5.1 5.1l-80.4 26.8 57.4-57.4c15.6-15.6 20.6-39 12.7-59.7L430.4 15.4C425.6 3 411.8-3.2 399.4 1.6s-18.5 18.6-13.8 31l32.5 84.6c1.1 3 .4 6.3-1.8 8.5L368 174.1V160c0-31.8-18.6-59.3-45.5-72.2c-9.1-4.4-18.5 3.3-18.5 13.4V112c0 8.8-7.2 16-16 16s-16-7.2-16-16V101.2c0-10.1-9.4-17.7-18.5-13.4C226.6 100.7 208 128.2 208 160v14.1l-48.3-48.3c-2.2-2.2-2.9-5.6-1.8-8.5l32.5-84.6z"/></svg>`
        }
}