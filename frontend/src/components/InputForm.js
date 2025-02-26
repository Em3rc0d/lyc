// frontend/src/components/InputForm.js
import React, { useState } from 'react';
import {
    Box,
    Button,
    Input,
    Text,
    Alert,
    AlertIcon,
    VStack,
    Heading,
} from '@chakra-ui/react';

const API_URL = 'http://localhost:8000';

const InputForm = ({ onValidationResult, currentAutomata, automataData }) => {
    const [input, setInput] = useState('');
    const [error, setError] = useState('');
    const [validationResult, setValidationResult] = useState(null);

    const helpTexts = {
        AFND: {
            description: "Este autómata no determinista (AFND) puede tener múltiples transiciones posibles para un mismo símbolo y estado, o transiciones vacías (épsilon). Acepta cadenas si existe al menos un camino de validación.",
            examples: "Ejemplos válidos: para un AFND que acepta cadenas con 'a' seguido de 'b', ejemplos serían 'ab', 'aab', 'abb', 'aaab', etc."
        },
        AFD: {
            description: "Este autómata determinista (AFD) tiene una única transición definida para cada símbolo y estado. Acepta cadenas si existe un camino de validación único y definido.",
            examples: "Ejemplos válidos: para un AFD que acepta cadenas con 'a' seguido de 'b', el único ejemplo válido sería 'ab'."
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setValidationResult(null);

        if (!/^[ab]*$/.test(input)) {
            setError('La cadena solo puede contener los símbolos "a" y "b"');
            onValidationResult(false);
            return;
        }

        try {
            console.log('Sending data:', {
                input: input,
                automataType: currentAutomata,
                automataData: {
                    nodes: automataData.nodes,
                    edges: automataData.edges
                }
            });

            const response = await fetch(`${API_URL}/api/validate/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input: input,
                    automataType: currentAutomata,
                    automataData: {
                        nodes: automataData.nodes,
                        edges: automataData.edges
                    }
                }),
            });

            console.log('Response:', response);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Data received:', data);
            
            // Mostrar el resultado de validación
            setValidationResult(data.isValid);
            
            if (data.error) {
                setError(data.error);
                onValidationResult(false);
            } else if (data.warnings && data.warnings.length > 0) {
                console.log('Warnings:', data.warnings); // Agrega esto para ver las advertencias
                setError('Advertencia: ' + data.warnings.join(', '));
                onValidationResult(data.isValid);
            } else {
                onValidationResult(data.isValid);
            }
        } catch (error) {
            console.error('Detailed error:', error);
            setError('Error al conectar con el servidor: ' + error.message);
        }
    };

    return (
        <VStack spacing={4} align="stretch">
            <Heading size="md">
                Validar Cadena en {currentAutomata}
            </Heading>

            {error && (
                <Alert status="error">
                    <AlertIcon />
                    {error}
                </Alert>
            )}

            {validationResult === true && !error && (
                <Alert status="success">
                    <AlertIcon />
                    ¡Cadena "{input}" válida! El autómata acepta esta cadena.
                </Alert>
            )}

            {validationResult === false && !error && (
                <Alert status="warning">
                    <AlertIcon />
                    Cadena "{input}" no válida. El autómata no acepta esta cadena.
                </Alert>
            )}

            <Text fontSize="sm" color="gray.600">
                {helpTexts[currentAutomata].description}
            </Text>

            <Box>
                <Input
                    value={input}
                    onChange={(e) => setInput(e.target.value.toLowerCase())}
                    placeholder="Ingrese la cadena a validar"
                    isInvalid={!!error}
                />
                <Text fontSize="sm" color="gray.500" mt={2}>
                    {error? '': helpTexts[currentAutomata].examples}
                </Text>
            </Box>

            <Button
                colorScheme="blue"
                onClick={handleSubmit}
                isDisabled={!input.length}
            >
                Validar
            </Button>
        </VStack>
    );
};

export default InputForm;