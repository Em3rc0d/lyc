import { extendTheme } from '@chakra-ui/react';
import { mode } from '@chakra-ui/theme-tools';

const theme = extendTheme({
  config: {
    initialColorMode: 'light',
    useSystemColorMode: false,
  },
  colors: {
    brand: {
      50: '#e3f2fd',
      100: '#bbdefb',
      200: '#90caf9',
      300: '#64b5f6',
      400: '#42a5f5',
      500: '#2196f3', // primary color
      600: '#1e88e5',
      700: '#1976d2',
      800: '#1565c0',
      900: '#0d47a1',
    },
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: 'semibold',
      },
      defaultProps: {
        colorScheme: 'brand',
      },
    },
  },
  styles: {
    global: props => ({
      body: {
        bg: mode('gray.100', 'gray.900')(props),
        color: mode('black', 'white')(props),
      },
    }),
  },
});

export default theme;
