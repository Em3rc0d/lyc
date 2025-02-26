import React, { useState } from 'react';
import { Box, Button, Input, VStack, HStack, Text, Heading, List, ListItem, 
         FormControl, FormLabel, FormErrorMessage, Select, Switch } from '@chakra-ui/react';

const EditorPanel = ({ nodes, edges, addNode, updateNode, deleteNode, addEdge, deleteEdge, undo, redo }) => {
  // Formularios locales para agregar estado o transición
  const [nuevoEstado, setNuevoEstado] = useState('');
  const [origen, setOrigen] = useState('');
  const [destino, setDestino] = useState('');
  const [simbolo, setSimbolo] = useState('');
  const [edgeError, setEdgeError] = useState('');

  // Función para cambiar el estado inicial
  const handleInitialStateChange = (nodeId) => {
    const newNodes = nodes.map(n => ({
      ...n,
      initial: n.id === nodeId
    }));
    updateNode(nodeId, { initial: true });
  };
  
  // Función para cambiar el estado final
  const handleFinalStateChange = (nodeId, isFinal) => {
    updateNode(nodeId, { final: isFinal });
  };

  const handleAddEdge = () => {
    if (!origen || !destino || !simbolo) {
      setEdgeError('Todos los campos son requeridos');
      return;
    }

    const success = addEdge(origen, destino, simbolo);
    if (success) {
      setOrigen('');
      setDestino('');
      setSimbolo('');
      setEdgeError('');
    }
  };

  return (
    <Box p={4} border="1px solid" borderColor="gray.300" borderRadius="md">
      <Heading size="md" mb={2}>Editor de Estados</Heading>
      <VStack spacing={2} align="stretch">
        <HStack>
          <Input
            value={nuevoEstado}
            onChange={(e) => setNuevoEstado(e.target.value)}
            placeholder="Nombre del estado"
          />
          <Button onClick={() => { addNode && addNode(nuevoEstado, 0, 0, false); setNuevoEstado(''); }}>Agregar</Button>
        </HStack>
        <List spacing={1}>
          {nodes.map(node => (
            <ListItem key={node.id} p={2} borderWidth="1px" borderRadius="md">
              <HStack justify="space-between">
                <Text fontWeight={node.initial ? 'bold' : 'normal'} 
                      color={node.initial ? 'orange.500' : 'inherit'}>
                  {node.id}
                  {node.initial && ' (Inicial)'}
                  {node.final && ' (Final)'}
                </Text>
                <HStack>
                  <Button 
                    size="xs" 
                    colorScheme={node.initial ? 'orange' : 'gray'}
                    onClick={() => handleInitialStateChange(node.id)}>
                    Inicial
                  </Button>
                  <Switch 
                    isChecked={node.final} 
                    onChange={(e) => handleFinalStateChange(node.id, e.target.checked)} 
                    colorScheme="red"
                    size="sm"
                  />
                  <Text fontSize="sm">Final</Text>
                  <Button 
                    size="xs" 
                    colorScheme="red" 
                    onClick={() => deleteNode(node.id)}>
                    Eliminar
                  </Button>
                </HStack>
              </HStack>
            </ListItem>
          ))}
        </List>
      </VStack>
      <Heading size="md" mt={4} mb={2}>Editor de Transiciones</Heading>
      <VStack spacing={2} align="stretch">
        <FormControl isInvalid={!!edgeError}>
          <HStack>
            <Select
              value={origen}
              onChange={(e) => setOrigen(e.target.value)}
              placeholder="Estado origen"
            >
              {nodes.map(node => (
                <option key={node.id} value={node.id}>{node.label}</option>
              ))}
            </Select>
            <Select
              value={destino}
              onChange={(e) => setDestino(e.target.value)}
              placeholder="Estado destino"
            >
              {nodes.map(node => (
                <option key={node.id} value={node.id}>{node.label}</option>
              ))}
            </Select>
            <Input
              value={simbolo}
              onChange={(e) => setSimbolo(e.target.value)}
              placeholder="Símbolo"
            />
            <Button onClick={handleAddEdge}>Agregar</Button>
          </HStack>
          {edgeError && <FormErrorMessage>{edgeError}</FormErrorMessage>}
        </FormControl>
        <List spacing={1}>
          {edges.map((edge, index) => (
            <ListItem key={index}>
              <HStack justify="space-between">
                <Text>{edge.from} → {edge.to} ({edge.label})</Text>
                <Button size="xs" colorScheme="red" onClick={() => deleteEdge && deleteEdge(edge.from, edge.to)}>Eliminar</Button>
              </HStack>
            </ListItem>
          ))}
        </List>
      </VStack>
      <HStack mt={4}>
        <Button onClick={undo}>Deshacer</Button>
        <Button onClick={redo}>Rehacer</Button>
      </HStack>
    </Box>
  );
};

export default EditorPanel;
