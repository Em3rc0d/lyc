import React from 'react';
import { Box, Container, Heading, Grid, GridItem, Button, VStack } from '@chakra-ui/react';
import AutomataVisualizer from './components/AutomataVisualizer';
import InputForm from './components/InputForm';
import { useAutomataLogic } from './hooks/useAutomataLogic';
import AutomataTypeSelector from './components/AutomataTypeSelector';
import AddNodeForm from './components/AddNodeForm';
import EditorPanel from './components/EditorPanel';

function App() {
    const { 
        nodes, 
        edges, 
        error, 
        convertAutomata, 
        addNode, 
        setNodes, 
        setEdges, 
        automataType, 
        setAutomataType, 
        alphabet, 
        setAlphabet,
        updateNode,
        deleteNode,
        addEdge,
        deleteEdge,
        undo,
        redo,
        canUndo,
        canRedo
    } = useAutomataLogic();

    const handleNodeSelect = (nodeId) => {
        console.log('Node selected:', nodeId);
    };

    const handleEdgeSelect = (edgeId) => {
        console.log('Edge selected:', edgeId);
    };

    const handleConvertClick = async () => {
        const afdData = await convertAutomata();
        if (afdData) {
            setNodes(afdData.nodes);
            setEdges(afdData.edges);
        }
    };

    return (
        <Container maxW="container.xl" py={8}>
            <Heading as="h1" size="xl" textAlign="center" mb={8}>
                Visualizador de Autómatas
            </Heading>
            {error && <Box color="red.500">{error}</Box>}
            
            <Grid templateColumns="3fr 1fr" gap={6}>
                <GridItem>
                    <VStack spacing={8} align="stretch">
                        <AutomataTypeSelector
                            automataType={automataType || 'AFND'}
                            setAutomataType={setAutomataType}
                            alphabet={alphabet || ['a', 'b']}
                            setAlphabet={setAlphabet}
                        />
                        <AutomataVisualizer
                            nodes={nodes}
                            edges={edges}
                            onNodeSelect={handleNodeSelect}
                            onEdgeSelect={handleEdgeSelect}
                        />
                        <InputForm
                            currentAutomata={automataType}
                            automataData={{ nodes, edges }}
                            onValidationResult={(isValid) => console.log("Validation Result:", isValid)}
                        />
                    </VStack>
                </GridItem>
                
                <GridItem>
                    <EditorPanel
                        nodes={nodes}
                        edges={edges}
                        addNode={addNode}
                        updateNode={updateNode}
                        deleteNode={deleteNode}
                        addEdge={addEdge}
                        deleteEdge={deleteEdge}
                        undo={undo}
                        redo={redo}
                        canUndo={canUndo}
                        canRedo={canRedo}
                    />
                </GridItem>
            </Grid>
        </Container>
    );
}

export default App;