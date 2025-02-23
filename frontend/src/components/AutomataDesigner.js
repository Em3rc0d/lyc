import React, { useEffect, useRef, useState, useCallback } from 'react';
import Cytoscape from 'cytoscape';
import cola from 'cytoscape-cola';
import {
    Box,
    Button,
    Input,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    FormControl,
    FormLabel,
    Checkbox,
    useToast,
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
} from '@chakra-ui/react';
import { useAutomataLogic } from '../hooks/useAutomataLogic';

Cytoscape.use(cola);

const AutomataDesigner = ({ onAutomataChange }) => {
    const containerRef = useRef(null);
    const cyRef = useRef(null);
    const layoutRef = useRef(null);  // Nueva referencia para el layout
    const toast = useToast();
    
    const {
        nodes,
        edges,
        addNode,
        addEdge,
        updateNode,
        deleteNode,
        deleteEdge,
        setInitialState,
        resetAutomata,
        error,
    } = useAutomataLogic(onAutomataChange);

    const [contextMenu, setContextMenu] = useState({
        visible: false,
        x: 0,
        y: 0,
        nodeId: null,
    });
    
    const [edgeDialog, setEdgeDialog] = useState({
        visible: false,
        source: null,
        target: null,
        symbol: '',
    });

    const safeRunLayout = useCallback(() => {
        if (!layoutRef.current || !cyRef.current || !containerRef.current) return;
        
        try {
            layoutRef.current.run();
        } catch (e) {
            console.error('Error running layout:', e);
        }
    }, []);

    const safeUpdateNode = useCallback((nodeId, changes) => {
        requestAnimationFrame(() => {
            if (cyRef.current) {
                updateNode(nodeId, changes);
            }
        });
    }, [updateNode]);

    const layoutConfig = useCallback(() => ({
        name: 'cola',
        fit: true,
        padding: 50,
        animate: false, // Deshabilitar animación para evitar problemas
        randomize: false,
        maxSimulationTime: 1000, // Reducir tiempo de simulación
        infinite: false,
        refresh: 30, // Reducir frecuencia de refresco
        nodeSpacing: 50,
        edgeLength: 100,
        unconstrIter: 1, // Reducir iteraciones
        userConstIter: 1, // Reducir iteraciones
        allConstIter: 1, // Reducir iteraciones
        ready: function() {
            // Layout está listo pero no ha comenzado
            if (!cyRef.current) return;
            cyRef.current.center();
            cyRef.current.fit();
        },
        stop: function() {
            // Layout ha terminado o sido detenido
            if (!cyRef.current) return;
            cyRef.current.center();
            cyRef.current.fit();
        }
    }), []);

    const initCytoscape = useCallback(() => {
        if (!containerRef.current) return;

        // Limpiar instancia anterior
        if (cyRef.current) {
            if (layoutRef.current) {
                try {
                    layoutRef.current.stop();
                } catch (e) {
                    console.error('Error stopping previous layout:', e);
                }
                layoutRef.current = null;
            }
            cyRef.current.destroy();
            cyRef.current = null;
        }

        const cy = Cytoscape({
            container: containerRef.current,
            elements: {
                nodes: nodes.map(n => ({ data: { ...n } })),
                edges: edges.map(e => ({ data: { ...e } }))
            },
            style: [
                {
                    selector: 'node',
                    style: {
                        'label': 'data(label)',
                        'width': 40,
                        'height': 40,
                        'background-color': '#fff',
                        'border-width': 3,
                        'border-color': (ele) => ele.data('initial') ? '#4CAF50' : '#2196F3',
                        'border-style': (ele) => ele.data('final') ? 'double' : 'solid',
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'label': 'data(label)',
                        'width': 2,
                        'line-color': '#666',
                        'target-arrow-color': '#666',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        'text-rotation': 'autorotate'
                    }
                }
            ],
            layout: layoutConfig() // Usar la configuración del layout
        });

        cyRef.current = cy;

        // Event handlers con verificaciones de seguridad
        const handlers = {
            'tap': (e) => {
                if (!cyRef.current || e.target !== cyRef.current) return;
                if (e.originalEvent.detail === 2) {
                    // Usar directamente las propiedades x,y del evento
                    const pos = e.position || { x: 0, y: 0 };
                    addNode({
                        id: `q${nodes.length}`,
                        label: `q${nodes.length}`,
                        x: pos.x,
                        y: pos.y
                    });
                }
                setContextMenu({ visible: false, x: 0, y: 0, nodeId: null });
            },
            'tap node': (e) => {
                if (!cyRef.current) return;
                const node = e.target;
                // Obtener la posición renderizada como objeto
                const renderedPos = node.renderedPosition();
                const nodeData = node.data();
                setContextMenu({
                    visible: true,
                    x: renderedPos.x,
                    y: renderedPos.y,
                    nodeId: nodeData.id
                });
            },
            'cxttap node': (e) => {
                if (!cyRef.current) return;
                e.preventDefault();
                const node = e.target;
                const renderedPos = node.renderedPosition();
                const nodeData = node.data();
                setContextMenu({
                    visible: true,
                    x: renderedPos.x,
                    y: renderedPos.y,
                    nodeId: nodeData.id
                });
            },
            'tapdrag node': (e) => {
                if (!cyRef.current) return;
                const node = e.target;
                const nodeData = node.data();
                // Acceder a las propiedades de posición directamente
                const pos = {
                    x: node.position().x,
                    y: node.position().y
                };
                safeUpdateNode(nodeData.id, {
                    x: pos.x,
                    y: pos.y
                });
            },
            'tap edge': (e) => {
                if (!cyRef.current) return;
                const edge = e.target;
                const edgeData = edge.data();
                setEdgeDialog({
                    visible: true,
                    source: edgeData.source,
                    target: edgeData.target,
                    symbol: edgeData.label
                });
            }
        };

        // Registrar handlers de manera segura
        Object.entries(handlers).forEach(([event, handler]) => {
            cy.on(event, handler);
        });

        // Iniciar layout de manera segura
        try {
            layoutRef.current = cy.layout(layoutConfig());
            layoutRef.current.run();
        } catch (e) {
            console.error('Error running layout:', e);
        }

    }, [nodes, edges, addNode, layoutConfig, safeUpdateNode]);

    useEffect(() => {
        let isMounted = true;

        const init = () => {
            if (isMounted) {
                requestAnimationFrame(() => {
                    if (isMounted) {
                        initCytoscape();
                    }
                });
            }
        };

        init();

        return () => {
            isMounted = false;
            if (layoutRef.current) {
                try {
                    layoutRef.current.stop();
                } catch (e) {
                    console.error('Error stopping layout:', e);
                }
                layoutRef.current = null;
            }
            if (cyRef.current) {
                try {
                    cyRef.current.removeAllListeners();
                    cyRef.current.destroy();
                } catch (e) {
                    console.error('Error destroying cytoscape:', e);
                }
                cyRef.current = null;
            }
        };
    }, [initCytoscape]);

    const handleCreateEdge = useCallback((source, target, symbol) => {
        if (!symbol) {
            toast({ title: 'Error', description: 'El símbolo no puede estar vacío', status: 'error' });
            return;
        }
        addEdge({ source, target, label: symbol === 'ε' ? 'ε' : symbol });
    }, [addEdge, toast]);

    const handleSetInitialState = useCallback((nodeId) => {
        setInitialState(nodeId);
        toast({ title: 'Estado inicial actualizado', status: 'success' });
    }, [setInitialState, toast]);

    const handleToggleFinalState = useCallback((nodeId) => {
        const node = nodes.find(n => n.id === nodeId);
        updateNode(nodeId, { final: !node.final });
    }, [nodes, updateNode]);

    return (
        <Box position="relative" h="600px" w="100%">
            <Box ref={containerRef} h="100%" w="100%" borderWidth={1} borderRadius="md" bg="white" />

            {contextMenu.visible && (
                <Box
                    position="absolute"
                    left={`${contextMenu.x}px`}
                    top={`${contextMenu.y}px`}
                    zIndex={1000}
                >
                    <Menu isOpen>
                        <MenuButton as={Box} />
                        <MenuList>
                            <MenuItem onClick={() => handleSetInitialState(contextMenu.nodeId)}>
                                Marcar como inicial
                            </MenuItem>
                            <MenuItem onClick={() => handleToggleFinalState(contextMenu.nodeId)}>
                                Toggle estado final
                            </MenuItem>
                            <MenuItem onClick={() => deleteNode(contextMenu.nodeId)} color="red.500">
                                Eliminar nodo
                            </MenuItem>
                        </MenuList>
                    </Menu>
                </Box>
            )}

            <Modal
                isOpen={edgeDialog.visible}
                onClose={() => setEdgeDialog(p => ({ ...p, visible: false }))}
            >
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Transición {edgeDialog.source} → {edgeDialog.target}</ModalHeader>
                    <ModalBody>
                        <FormControl>
                            <FormLabel>Símbolo de transición:</FormLabel>
                            <Input
                                autoFocus
                                value={edgeDialog.symbol}
                                onChange={(e) => setEdgeDialog(p => ({ ...p, symbol: e.target.value }))}
                                placeholder="Ej: a, b, ε"
                            />
                        </FormControl>
                    </ModalBody>
                    <ModalFooter>
                        <Button
                            colorScheme="blue"
                            onClick={() => {
                                handleCreateEdge(edgeDialog.source, edgeDialog.target, edgeDialog.symbol);
                                setEdgeDialog(p => ({ ...p, visible: false }));
                            }}
                        >
                            Guardar
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>

            <Box position="absolute" top={2} right={2} display="flex" gap={2}>
                <Button colorScheme="blue" onClick={() => resetAutomata()}>
                    Reiniciar
                </Button>
            </Box>
        </Box>
    );
};

export default AutomataDesigner;