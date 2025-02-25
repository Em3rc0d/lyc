import React from 'react';
import { HStack, Button } from '@chakra-ui/react';

const Toolbar = ({ network }) => {
    const zoomIn = () => { if (network) network.moveTo({ scale: network.getScale() * 1.2 }); };
    const zoomOut = () => { if (network) network.moveTo({ scale: network.getScale() / 1.2 }); };
    const resetView = () => { if (network) network.fit(); };

    return (
        <HStack spacing={4} mb={4}>
            <Button onClick={zoomIn}>Zoom In</Button>
            <Button onClick={zoomOut}>Zoom Out</Button>
            <Button onClick={resetView}>Resetear Vista</Button>
        </HStack>
    );
};

export default Toolbar;
