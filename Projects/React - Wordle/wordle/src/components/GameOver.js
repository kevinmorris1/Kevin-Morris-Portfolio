import React, { useContext } from 'react'
import { AppContext } from '../App'

function GameOver() {
    const {gameOver, currAttempt, correctWord} = useContext(AppContext);

    const playAgain = () => {
        window.location.reload();
     }

    return (
        <div className='gameOver'>
            <h3>{gameOver.guessedWord ? "You Win!" : " You Failed"}</h3>
            <h1>Correct: {correctWord}</h1>
            <div>{gameOver.guessedWord && (<h3>You guessed in {currAttempt.attempt} attemps</h3>)}</div>
            <div><button onClick={playAgain}>Play Again</button></div>
        </div>
    )
}

export default GameOver