import React from 'react';
import { Box, Button, Popover, PopoverTrigger, PopoverContent, PopoverArrow, PopoverBody, VStack } from '@chakra-ui/react';

const ContextMenu = ({ children, options, onSelect }) => {
  // options es un array de { label, value }
  return (
    <Popover placement="right-start" closeOnBlur>
      <PopoverTrigger>
        <Box onContextMenu={(e) => { e.preventDefault(); }}>
          {children}
        </Box>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverArrow />
        <PopoverBody>
          <VStack align="stretch">
            {options.map(opt => (
              <Button key={opt.value} variant="ghost" onClick={() => onSelect(opt.value)}>
                {opt.label}
              </Button>
            ))}
          </VStack>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
};

export default ContextMenu;
