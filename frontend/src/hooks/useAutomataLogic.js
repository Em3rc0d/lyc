import { useState, useCallback } from 'react';

export const useAutomataLogic = (onAutomataChange) => {
    const [nodes, setNodes] = useState([]);
    const [edges, setEdges] = useState([]);
    const [error, setError] = useState(null);

    // Initialize with a default node 'q0' if nodes array is empty
    useState(() => {
        if (nodes.length === 0) {
            setNodes([{ id: 'q0', label: 'q0', shape: 'circle' }]);
        }
    }, []); // Empty dependency array ensures this runs only once on initial mount


    const validateNodeName = useCallback((name) => {
        if (!name.trim()) {
            throw new Error('El nombre del estado no puede estar vacío.');
        }
        if (nodes.some(node => node.id === name)) {
            throw new Error('Ya existe un estado con ese nombre.');
        }
        if (!/^[a-zA-Z0-9_]+$/.test(name)) {
            throw new Error('Nombre de estado inválido. Use solo letras, números y guiones bajos.');
        }
        return true; // Indicate validation success
    }, [nodes]);


    const addNode = useCallback((name, isFinal) => {
        try {
            validateNodeName(name); // Validate node name before adding
            const newNode = {
                id: name,
                label: name,
                shape: isFinal ? 'doublecircle' : 'circle'
            };
            setNodes(prevNodes => [...prevNodes, newNode]);
            setError(null);
            return true; // Indicate node addition success
        } catch (err) {
            setError(err.message);
            return false; // Indicate node addition failure
        }
    }, [validateNodeName, setNodes, setError]);


    const addEdge = useCallback((from, to, symbol) => {
        if (!symbol.trim()) {
            setError('El símbolo de transición no puede estar vacío.');
            return false;
        }

        const newEdge = { from, to, label: symbol };
        setEdges(prevEdges => [...prevEdges, newEdge]);
        setError(null);
        return true; // Indicate edge addition success
    }, [setEdges, setError]);

    const updateNode = useCallback((id, changes) => {
        setNodes(prev =>
            prev.map(node => node.id === id ? { ...node, ...changes } : node)
        );
    }, [setNodes]);

    const deleteNode = useCallback((nodeId) => {
        setNodes(prev => prev.filter(n => n.id !== nodeId));
        setEdges(prev => prev.filter(e => e.from !== nodeId && e.to !== nodeId));
    }, [setNodes, setEdges]);

    const deleteEdge = useCallback((from, to) => {
        setEdges(prev => prev.filter(e => !(e.from === from && e.to === to)));
    }, [setEdges]);

    const setInitialState = useCallback((nodeId) => {
        setNodes(prev =>
            prev.map(n => ({ ...n, initial: n.id === nodeId }))
        );
    }, [setNodes]);

    const resetAutomata = useCallback(() => {
        setNodes([]);
        setEdges([]);
    }, [setNodes, setEdges]);

    return {
        nodes,
        edges,
        error,
        addNode,
        addEdge,
        setNodes,
        setEdges,
        setError,
        validateNodeName, // Expose validateNodeName if needed elsewhere
        updateNode,
        deleteNode,
        deleteEdge,
        setInitialState,
        resetAutomata
    };
};