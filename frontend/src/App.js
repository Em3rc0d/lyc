import React, { useState } from 'react';
import {
    Container,
    Box,
    Heading,
    Tabs,
    TabList,
    TabPanels,
    Tab,
    TabPanel,
    VStack,
    Button,
    Text,
    useColorModeValue,
} from '@chakra-ui/react';
import AutomataVisualizer from './components/AutomataVisualizer';
import InputForm from './components/InputForm';
import AutomataDesigner from './components/AutomataDesigner';

function App() {
    const [tabIndex, setTabIndex] = useState(0);
    const [validationResult, setValidationResult] = useState(null);
    const [automataData, setAutomataData] = useState({
        nodes: [],
        edges: []
    });
    const [afdData, setAfdData] = useState(null);

    const bgColor = useColorModeValue('white', 'gray.800');
    const borderColor = useColorModeValue('gray.200', 'gray.700');

    const handleTabChange = (index) => {
        setTabIndex(index);
    };

    const handleAutomataChange = async (newData) => {
        setAutomataData(newData);
    };

    const handleConvertToAFD = async () => {
        try {
            const response = await fetch('http://localhost:5000/automata/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(automataData)
            });
            if (!response.ok) throw new Error('Error en la conversión');
            const afdResult = await response.json();
            setAfdData(afdResult);
        } catch (error) {
            console.error('Error al convertir el autómata:', error);
            // Consider adding user-facing error feedback here, like a Snackbar
        }
    };

    return (
        <Container maxW="container.xl" py={8}>
            <VStack spacing={8}>
                <Heading as="h1" size="xl" textAlign="center">
                    Visualizador de Autómatas
                </Heading>

                <Box w="full" bg={bgColor} borderRadius="lg" borderWidth="1px" p={6}>
                    <Tabs isFitted variant="enclosed" index={tabIndex} onChange={handleTabChange}>
                        <TabList mb={4}>
                            <Tab>AFND</Tab>
                            <Tab>AFD</Tab>
                        </TabList>

                        <TabPanels>
                            <TabPanel>
                                <AutomataVisualizer
                                    automataType="AFND"
                                    automataData={automataData}
                                />
                            </TabPanel>
                            <TabPanel>
                                <AutomataVisualizer
                                    automataType="AFD"
                                    automataData={afdData || { nodes: [], edges: [] }}
                                />
                            </TabPanel>
                        </TabPanels>
                    </Tabs>
                </Box>

                <Box w="full" bg={bgColor} borderRadius="lg" borderWidth="1px" p={6}>
                    <InputForm
                        onValidationResult={setValidationResult}
                        currentAutomata={tabIndex === 0 ? 'AFND' : 'AFD'}
                    />
                    {validationResult !== null && (
                        <Text
                            mt={4}
                            fontSize="lg"
                            color={validationResult ? "green.500" : "red.500"}
                            fontWeight="bold"
                        >
                            {validationResult
                                ? "¡La cadena es válida!"
                                : "La cadena no es válida."}
                        </Text>
                    )}
                </Box>

                <Box w="full" bg={bgColor} borderRadius="lg" borderWidth="1px" p={6}>
                    <VStack spacing={4}>
                        <Heading size="md">Diseñador de Autómatas</Heading>
                        <AutomataDesigner onAutomataChange={handleAutomataChange} />
                        <Button
                            colorScheme="purple"
                            onClick={handleConvertToAFD}
                            size="lg"
                        >
                            Convertir a AFD
                        </Button>
                    </VStack>
                </Box>
            </VStack>
        </Container>
    );
}

export default App;