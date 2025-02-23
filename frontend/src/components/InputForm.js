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

const InputForm = ({ onValidationResult, currentAutomata }) => {
    const [input, setInput] = useState('');
    const [error, setError] = useState('');

    // Help texts based on automata type
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

        // Validate that the string only contains 'a' and 'b'
        if (!/^[ab]*$/.test(input)) {
            setError('La cadena solo puede contener los símbolos "a" y "b"');
            onValidationResult(false); // Immediately indicate invalid input
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    input,
                    automataType: currentAutomata
                }),
            });

            const data = await response.json();

            if (response.ok) {
                onValidationResult(data.isValid);
            } else {
                setError(data.error || 'Error al validar la cadena');
                onValidationResult(false);
            }
        } catch (fetchError) {
            console.error('Error al validar:', fetchError);
            setError('Error de conexión con el servidor');
            onValidationResult(false);
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
                    {error ? '' : helpTexts[currentAutomata].examples}
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
