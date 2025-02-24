import React, { useState } from 'react';
import { Button, Input, VStack, Text } from '@chakra-ui/react';

const AddNodeForm = ({ addNode }) => {
    const [nodeName, setNodeName] = useState('');

    const handleAddNode = () => {
        if (!nodeName) return;
        const success = addNode(nodeName, 0, 0, false);
        if (success) setNodeName('');
    };

    return (
        <VStack align="start">
            <Text>Nombre del nuevo estado:</Text>
            <Input
                value={nodeName}
                onChange={(e) => setNodeName(e.target.value)}
                placeholder="Ej: q1"
            />
            <Button onClick={handleAddNode}>Agregar Nodo</Button>
        </VStack>
    );
};

export default AddNodeForm;
