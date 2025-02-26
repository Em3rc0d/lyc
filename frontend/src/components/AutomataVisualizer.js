import React, { useEffect, useRef } from 'react';
import { Network } from 'vis-network';
import { DataSet } from 'vis-data';

const AutomataVisualizer = ({ nodes, edges, onNodeSelect, onEdgeSelect, onNodePositionChange }) => {
    const containerRef = useRef(null);
    const networkRef = useRef(null);

    useEffect(() => {
        if (!containerRef.current) return;

        // Convertir los nodos al formato de vis.js
        const visNodes = new DataSet(nodes.map(node => ({
            id: node.id,
            label: node.label,
            // Usar doublecircle para estados finales
            shape: node.final ? 'doublecircle' : 'circle',
            size: 30,
            color: {
                // Color diferente para estados iniciales
                background: node.initial ? '#FFA726' : '#ffffff', 
                border: node.final ? '#D32F2F' : '#2B7CE9',
                highlight: {
                    background: node.initial ? '#FFB74D' : '#D2E5FF',
                    border: node.final ? '#F44336' : '#2B7CE9'
                }
            },
            // Borde más grueso para estados finales
            borderWidth: node.final ? 3 : 1,
            // Añadir una flecha de entrada para el estado inicial
            shapeProperties: {
                borderDashes: node.initial ? [5, 5] : false,
                useImageSize: false,
                useBorderWithImage: true
            },
            // Tooltip mejorado
            title: `Estado: ${node.id} ${node.initial ? '(Inicial)' : ''} ${node.final ? '(Final)' : ''}`
        })));

        // Convertir las aristas al formato de vis.js
        const visEdges = new DataSet(edges.map(edge => ({
            id: edge.id || `${edge.from}-${edge.to}-${edge.label}`,
            from: edge.from,
            to: edge.to,
            label: edge.label,
            arrows: 'to',
            font: { 
                align: 'horizontal',
                size: 12,
                color: '#343434',
                face: 'arial'
            },
            color: {
                color: '#848484',
                highlight: '#848484',
                hover: '#848484'
            },
            smooth: {
                enabled: true,
                type: 'curvedCW',
                roundness: 0.2
            },
            width: 2,
            title: `De ${edge.from} a ${edge.to} (${edge.label})` // Tooltip
        })));

        // Configuración de la red
        const options = {
            nodes: {
                font: { size: 20 }
            },
            edges: {
                font: { size: 16 },
                smooth: {
                    enabled: true,
                    type: 'curvedCW',
                    roundness: 0.2
                },
                arrows: {
                    to: { enabled: true, scaleFactor: 1 }
                }
            },
            physics: {
                enabled: true,
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {
                    gravitationalConstant: -26,
                    centralGravity: 0.005,
                    springLength: 230,
                    springConstant: 0.18
                },
                stabilization: {
                    enabled: true,
                    iterations: 1000,
                    updateInterval: 100
                }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200
            }
        };

        // Crear la red
        networkRef.current = new Network(
            containerRef.current,
            { nodes: visNodes, edges: visEdges },
            options
        );

        // Añadir una flecha especial para marcar el estado inicial
        setTimeout(() => {
            const initialNode = nodes.find(node => node.initial);
            if (initialNode && networkRef.current) {
                const initialNodePosition = networkRef.current.getPositions([initialNode.id])[initialNode.id];
                if (initialNodePosition) {
                    visEdges.add({
                        id: 'initial-arrow',
                        from: { x: initialNodePosition.x - 60, y: initialNodePosition.y },
                        to: initialNode.id,
                        arrows: 'to',
                        color: { color: '#FFA726' },
                        width: 2,
                        length: 60,
                        label: 'inicio',
                        font: { align: 'bottom' },
                        physics: false,
                        smooth: { enabled: false }
                    });
                }
            }
        }, 100); // Pequeño retraso para asegurar que la red ha calculado las posiciones

        // Eventos
        if (networkRef.current) {
            networkRef.current.on('selectNode', params => {
                if (onNodeSelect) onNodeSelect(params.nodes[0]);
            });

            networkRef.current.on('selectEdge', params => {
                if (onEdgeSelect) onEdgeSelect(params.edges[0]);
            });

            // Nuevo evento para actualizar posiciones tras arrastrar nodos
            networkRef.current.on('dragEnd', params => {
                if (params.nodes.length > 0 && onNodePositionChange) {
                    const positions = networkRef.current.getPositions(params.nodes);
                    onNodePositionChange(positions);
                    
                    // Actualizar la posición de la flecha inicial si es necesario
                    const initialNode = nodes.find(node => node.initial);
                    if (initialNode && params.nodes.includes(initialNode.id)) {
                        const initialNodePosition = positions[initialNode.id];
                        visEdges.update({
                            id: 'initial-arrow',
                            from: { x: initialNodePosition.x - 60, y: initialNodePosition.y }
                        });
                    }
                }
            });
        }

        return () => {
            if (networkRef.current) {
                networkRef.current.destroy();
                networkRef.current = null;
            }
        };
    }, [nodes, edges, onNodeSelect, onEdgeSelect, onNodePositionChange]);

    return (
        <div 
            ref={containerRef} 
            style={{ 
                height: '600px', 
                border: '1px solid #ddd',
                borderRadius: '8px',
                background: 'white' 
            }} 
        />
    );
};

export default AutomataVisualizer;