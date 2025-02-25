import React from 'react';
import { Select, Input, VStack, Text } from '@chakra-ui/react';

const AutomataTypeSelector = ({ automataType, setAutomataType, alphabet = ['a', 'b'], setAlphabet }) => {
    const handleAlphabetChange = (e) => {
        const value = e.target.value.split(',').map(sym => sym.trim()).filter(Boolean);
        setAlphabet(value);
    };

    return (
        <VStack align="stretch" spacing={4}>
            <Text>Tipo de Autómata:</Text>
            <Select value={automataType} onChange={(e) => setAutomataType(e.target.value)}>
                <option value="AFND">AFND</option>
                <option value="AFD">AFD</option>
                <option value="PDA">PDA</option>
                <option value="TM">TM</option>
            </Select>
            <Text>Alfabeto (separar con comas):</Text>
            <Input 
                value={Array.isArray(alphabet) ? alphabet.join(', ') : 'a, b'} 
                onChange={handleAlphabetChange}
                placeholder="Ejemplo: a, b, c"
            />
        </VStack>
    );
};

export default AutomataTypeSelector;
