import React, { useEffect, useRef, useCallback } from 'react';
import Cytoscape from '../cytoscapeConfig';
import { Box } from '@chakra-ui/react';

const AutomataVisualizer = ({ automataType, automataData }) => {
    const containerRef = useRef(null);
    const cyRef = useRef(null);
    const layoutRef = useRef(null);

    const safeRunLayout = useCallback(() => {
        if (!layoutRef.current || !cyRef.current || !containerRef.current) return;
        
        try {
            layoutRef.current.run();
        } catch (e) {
            console.error('Error running layout:', e);
        }
    }, []);

    useEffect(() => {
        if (!automataData || !containerRef.current) return;

        let isComponentMounted = true;
        let cleanup = () => {};

        const initCytoscape = () => {
            try {
                if (containerRef.current.offsetWidth === 0 || containerRef.current.offsetHeight === 0) {
                    return;
                }

                const cytoscapeElements = {
                    nodes: automataData.nodes.map(node => ({
                        data: {
                            id: node.id,
                            label: node.label,
                            isFinal: node.shape === 'doublecircle'
                        }
                    })),
                    edges: automataData.edges.map(edge => ({
                        data: {
                            id: `${edge.from}-${edge.to}`,
                            source: edge.from,
                            target: edge.to,
                            label: edge.label
                        }
                    }))
                };

                if (cyRef.current) {
                    cyRef.current.destroy();
                }

                const cy = Cytoscape({
                    container: containerRef.current,
                    elements: cytoscapeElements,
                    style: [
                        {
                            selector: 'node',
                            style: {
                                'background-color': '#fff',
                                'border-color': '#2196f3',
                                'border-width': 2,
                                'label': 'data(label)',
                                'text-valign': 'center',
                                'text-halign': 'center',
                                'width': 40,
                                'height': 40
                            }
                        },
                        {
                            selector: 'node[?isFinal]',
                            style: {
                                'border-width': 4,
                                'border-style': 'double'
                            }
                        },
                        {
                            selector: 'edge',
                            style: {
                                'width': 2,
                                'line-color': '#666',
                                'target-arrow-color': '#666',
                                'target-arrow-shape': 'triangle',
                                'curve-style': 'bezier',
                                'label': 'data(label)'
                            }
                        }
                    ],
                    layout: {
                        name: 'preset',
                        fit: true,
                        padding: 50,
                        animate: false
                    }
                });

                layoutRef.current = cy.layout({
                    name: 'preset',
                    fit: true,
                    padding: 50,
                    animate: false,
                    maxSimulationTime: 1000,
                    stop: () => {
                        if (!isComponentMounted) return;
                        if (cyRef.current) {
                            cyRef.current.center();
                            cyRef.current.fit();
                        }
                    }
                });

                if (isComponentMounted) {
                    safeRunLayout();
                }

                cyRef.current = cy;
            } catch (e) {
                console.error('Error in cytoscape initialization:', e);
            }
        };

        cleanup = () => {
            isComponentMounted = false;

            if (layoutRef.current) {
                try {
                    layoutRef.current.stop();
                } catch (e) {
                    console.error('Error stopping layout:', e);
                } finally {
                    layoutRef.current = null;
                }
            }

            if (cyRef.current) {
                try {
                    cyRef.current.removeAllListeners();
                    cyRef.current.destroy();
                } catch (e) {
                    console.error('Error destroying cytoscape:', e);
                } finally {
                    cyRef.current = null;
                }
            }
        };

        initCytoscape();
        return cleanup;
    }, [automataData, safeRunLayout]);

    return (
        <Box position="relative">
            <Box
                ref={containerRef}
                h="600px"
                border="1px solid"
                borderColor="gray.200"
                borderRadius="lg"
                bg="gray.50"
                boxShadow="sm"
                overflow="hidden"
            />
        </Box>
    );
};

export default AutomataVisualizer;