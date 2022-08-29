import React, {useContext} from 'react';
import {AppContext} from '../App';

function Key({keyVal, bigKey, disabled, accurate, alternate}) {
    const {board, setBoard, currAttempt, setCurrAttempt, onSelectLetter, onEnter, onDelete} = useContext(AppContext);
    const selectLetter = () => {
        if (keyVal === 'ENTER') {
            onEnter();
        } else if (keyVal === 'DELETE') {
            onDelete();
        } else {
            onSelectLetter(keyVal);
        }
    }
  return (
    <div className='key' id={bigKey ? "big" : accurate ? "accurate" : alternate ? "alternate" : disabled && "disabled"} onClick={selectLetter}>
        {keyVal}
    </div>
  )
}

export default Key