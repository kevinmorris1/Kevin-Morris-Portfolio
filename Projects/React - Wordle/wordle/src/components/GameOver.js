import React, { useContext } from 'react'
import { AppContext } from '../App'

function GameOver() {
    const {gameOver, currAttempt, correctWord} = useContext(AppContext);

    const playAgain = () => {
        window.location.reload();
     }

    return (
        <div className='gameOver'>
            <h3>{gameOver.guessedWord ? "You won the game!" : "You failed"}</h3>
            <h1>Correct Word: {correctWord}</h1>
            <div>{gameOver.guessedWord && (<h3>You guessed in {currAttempt.attempt} attemps</h3>)}</div>
            <div><button onClick={playAgain}>Play Again</button></div>
        </div>
    )
}

export default GameOver