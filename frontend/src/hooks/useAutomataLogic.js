// frontend/src/hooks/useAutomataLogic.js
import { useState, useCallback } from 'react';
import { useHistory } from './useHistory';

export const useAutomataLogic = (onAutomataChange) => {
    const [nodes, setNodes] = useState([{
        id: 'q0',
        label: 'q0',
        shape: 'circle',
        final: false,
        initial: true, // Marca el estado inicial
        x: 0,
        y: 0
    }]);
    const [edges, setEdges] = useState([]);
    const [error, setError] = useState(null);
    const [automataType, setAutomataType] = useState('AFND');
    const [alphabet, setAlphabet] = useState(['a', 'b']); // Inicializar con valores por defecto
    const { pushState, undo, redo, canUndo, canRedo } = useHistory({ nodes: [], edges: [] });

    const handleStateChange = useCallback((newNodes, newEdges) => {
        setNodes(newNodes);
        setEdges(newEdges);
        pushState({ nodes: newNodes, edges: newEdges });
    }, [pushState]);

    const handleUndo = useCallback(() => {
        const prevState = undo();
        if (prevState) {
            setNodes(prevState.nodes);
            setEdges(prevState.edges);
        }
    }, [undo]);

    const handleRedo = useCallback(() => {
        const nextState = redo();
        if (nextState) {
            setNodes(nextState.nodes);
            setEdges(nextState.edges);
        }
    }, [redo]);

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

    const addNode = useCallback((id, x, y, isFinal) => {
        try {
            validateNodeName(id); // Validar el id del nodo
            const newNode = {
                id,
                label: id,
                shape: isFinal ? 'doublecircle' : 'circle',
                final: isFinal,
                x,
                y
            };
            const newNodes = [...nodes, newNode];
            handleStateChange(newNodes, edges);
            setError(null);
            return true;
        } catch (err) {
            setError(err.message);
            return false;
        }
    }, [validateNodeName, nodes, edges, handleStateChange]);

    const validateEdge = useCallback((from, to, symbol) => {
        if (!from || !to) {
            throw new Error('Los estados de origen y destino son requeridos.');
        }
        if (!symbol || !symbol.trim()) {
            throw new Error('El símbolo de transición es requerido.');
        }
        if (!nodes.some(n => n.id === from)) {
            throw new Error(`El estado de origen "${from}" no existe.`);
        }
        if (!nodes.some(n => n.id === to)) {
            throw new Error(`El estado de destino "${to}" no existe.`);
        }
        if (!alphabet.includes(symbol)) {
            throw new Error(`El símbolo "${symbol}" no pertenece al alfabeto.`);
        }
        return true;
    }, [nodes, alphabet]);

    const addEdge = useCallback((from, to, symbol) => {
        try {
            validateEdge(from, to, symbol);
            const newEdge = {
                id: `${from}-${to}-${symbol}`,
                from,
                to,
                label: symbol,
                arrows: 'to',
                smooth: { type: 'curvedCW', roundness: 0.2 }
            };
            const newEdges = [...edges, newEdge];
            handleStateChange(nodes, newEdges);
            setError(null);
            return true;
        } catch (err) {
            setError(err.message);
            return false;
        }
    }, [nodes, edges, validateEdge, handleStateChange]);

    const updateNode = useCallback((id, changes) => {
        const newNodes = nodes.map(node => node.id === id ? { ...node, ...changes } : node);
        handleStateChange(newNodes, edges);
    }, [nodes, edges, handleStateChange]);

    const deleteNode = useCallback((nodeId) => {
        const newNodes = nodes.filter(n => n.id !== nodeId);
        const newEdges = edges.filter(e => e.from !== nodeId && e.to !== nodeId);
        handleStateChange(newNodes, newEdges);
    }, [nodes, edges, handleStateChange]);

    const deleteEdge = useCallback((from, to) => {
        const newEdges = edges.filter(e => !(e.from === from && e.to === to));
        handleStateChange(nodes, newEdges);
    }, [nodes, edges, handleStateChange]);

    const setInitialState = useCallback((nodeId) => {
        const newNodes = nodes.map(n => ({ ...n, initial: n.id === nodeId }));
        handleStateChange(newNodes, edges);
    }, [nodes, edges, handleStateChange]);

    const resetAutomata = useCallback(() => {
        handleStateChange([], []);
    }, [handleStateChange]);

    const saveAutomata = useCallback(async () => {
        try {
            const response = await fetch('http://localhost:8000/api/automata/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nodes, edges }),
            });
            if (!response.ok) throw new Error('Error al guardar el autómata');
            return await response.json();
        } catch (err) {
            setError(err.message);
            return null;
        }
    }, [nodes, edges]);

     const convertAutomata = useCallback(async () => {
        try {
            const response = await fetch('http://localhost:3001/automata/convert', { // Backend endpoint for conversion
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ nodes, edges }), // Send current nodes and edges
            });
            if (!response.ok) {
                throw new Error('Error al convertir el autómata');
            }
            const data = await response.json();
            console.log("AFD Data received:", data); // Log the response
            setNodes(data.nodes); // Update nodes with AFD nodes
            setEdges(data.edges); // Update edges with AFD edges
            return data; // Return the converted automata data if needed
        } catch (err) {
            setError(err.message);
            return null;
        }
    }, [nodes, edges, setNodes, setEdges, setError]);

    const loadAutomata = useCallback(async () => {
        try {
            const response = await fetch('http://localhost:8000/api/automata/');
            if (!response.ok) throw new Error('Error al cargar el autómata');
            const data = await response.json();
            setNodes(data.nodes);
            setEdges(data.edges);
        } catch (err) {
            setError(err.message);
        }
    }, []);

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
        resetAutomata,
        saveAutomata,
        loadAutomata,
        convertAutomata,
        automataType,
        setAutomataType,
        alphabet,        // Asegurarse de que alphabet está incluido en el return
        setAlphabet,    // Asegurarse de que setAlphabet está incluido en el return
        undo: handleUndo,
        redo: handleRedo,
        canUndo,
        canRedo
    };
};