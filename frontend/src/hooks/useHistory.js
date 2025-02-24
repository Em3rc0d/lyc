import { useState, useCallback } from 'react';

export const useHistory = (initialState) => {
    const [history, setHistory] = useState([initialState]);
    const [currentIndex, setCurrentIndex] = useState(0);

    const pushState = useCallback((newState) => {
        const newHistory = history.slice(0, currentIndex + 1);
        newHistory.push(newState);
        setHistory(newHistory);
        setCurrentIndex(newHistory.length - 1);
    }, [history, currentIndex]);

    const undo = useCallback(() => {
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
            return history[currentIndex - 1];
        }
        return null;
    }, [history, currentIndex]);

    const redo = useCallback(() => {
        if (currentIndex < history.length - 1) {
            setCurrentIndex(currentIndex + 1);
            return history[currentIndex + 1];
        }
        return null;
    }, [history, currentIndex]);

    return { pushState, undo, redo, canUndo: currentIndex > 0, canRedo: currentIndex < history.length - 1 };
};
