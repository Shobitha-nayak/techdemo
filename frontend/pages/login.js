// import { useState } from 'react';
// import { useRouter } from 'next/router';
// import { useForm } from 'react-hook-form';
// import {
//   Box,
//   Button,
//   Container,
//   FormControl,
//   FormLabel,
//   Heading,
//   Input,
//   Stack,
//   Text,
//   useToast,
//   VStack,
//   HStack,
//   ChakraProvider,
// } from '@chakra-ui/react';

// export default function Login() {
//   const router = useRouter();
//   const [isLogin, setIsLogin] = useState(true);
//   const { register, handleSubmit, reset } = useForm();
//   const toast = useToast();

//   const onSubmit = (data) => {
//     const users = JSON.parse(localStorage.getItem('users')) || [];

//     if (isLogin) {
//       const user = users.find(user => user.email === data.email && user.password === data.password);
//       if (user) {
//         localStorage.setItem('isLoggedIn', true);
//         router.push('/');
//       } else {
//         toast({
//           title: "Invalid credentials",
//           status: "error",
//           duration: 3000,
//           isClosable: true,
//         });
//       }
//     } else {
//       users.push(data);
//       localStorage.setItem('users', JSON.stringify(users));
//       toast({
//         title: "Registration successful",
//         status: "success",
//         duration: 3000,
//         isClosable: true,
//       });
//       reset();
//       setIsLogin(true);
//     }
//   };

//   return (
//     <ChakraProvider>
//       <Container centerContent>
//         <Box
//           p={8}
//           mt={8}
//           borderWidth={1}
//           borderRadius="lg"
//           boxShadow="lg"
//           maxWidth="400px"
//           w="full"
//         >
//           <Heading as="h1" mb={6} textAlign="center">
//             {isLogin ? 'Login' : 'Register'}
//           </Heading>
//           <form onSubmit={handleSubmit(onSubmit)}>
//             <VStack spacing={4}>
//               {!isLogin && (
//                 <FormControl id="name" isRequired>
//                   <FormLabel>Name</FormLabel>
//                   <Input type="text" {...register('name', { required: true })} />
//                 </FormControl>
//               )}
//               <FormControl id="email" isRequired>
//                 <FormLabel>Email</FormLabel>
//                 <Input type="email" {...register('email', { required: true })} />
//               </FormControl>
//               <FormControl id="password" isRequired>
//                 <FormLabel>Password</FormLabel>
//                 <Input type="password" {...register('password', { required: true })} />
//               </FormControl>
//               <Button
//                 type="submit"
//                 colorScheme={isLogin ? 'teal' : 'blue'}
//                 width="full"
//               >
//                 {isLogin ? 'Login' : 'Register'}
//               </Button>
//             </VStack>
//           </form>
//           <HStack justify="center" mt={4}>
//             <Button variant="link" onClick={() => setIsLogin(!isLogin)}>
//               {isLogin ? 'Need to register?' : 'Already have an account?'}
//             </Button>
//           </HStack>
//         </Box>
//       </Container>
//     </ChakraProvider>
//   );
// }










import { useState } from 'react';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import {
  Box,
  Button,
  Container,
  FormControl,
  FormLabel,
  Heading,
  Input,
  VStack,
  HStack,
  useToast,
  ChakraProvider,
} from '@chakra-ui/react';

export default function Login() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const { register, handleSubmit, reset } = useForm();
  const toast = useToast();

  const onSubmit = (data) => {
    const users = JSON.parse(localStorage.getItem('users')) || [];

    if (isLogin) {
      const user = users.find(user => user.email === data.email && user.password === data.password);
      if (user) {
        localStorage.setItem('isLoggedIn', true);
        router.push('/');
      } else {
        toast({
          title: "Invalid credentials",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    } else {
      users.push(data);
      localStorage.setItem('users', JSON.stringify(users));
      toast({
        title: "Registration successful",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      reset();
      setIsLogin(true);
    }
  };

  return (
    <ChakraProvider>
      <Container centerContent>
        <Box
          p={10} // Increased padding for more space inside the box
          mt={10} // Increased margin top for spacing
          borderWidth={1}
          borderRadius="lg"
          boxShadow="lg"
          maxWidth="500px" // Increased max width for a larger box
          w="full"
          bg="white"
          borderColor="gray.200"
        >
          <Heading as="h1" mb={6} textAlign="center" color="teal.600">
            Welcome to the Stock Market Dashboard
          </Heading>
          <Box
            p={8} // Adjusted padding for the inner box
            borderWidth={1}
            borderRadius="lg"
            boxShadow="md"
            bg="gray.50"
            borderColor="gray.300"
          >
            <Heading as="h2" mb={4} textAlign="center" size="lg">
              {isLogin ? 'Login' : 'Register'}
            </Heading>
            <form onSubmit={handleSubmit(onSubmit)}>
              <VStack spacing={4}>
                {!isLogin && (
                  <FormControl id="name" isRequired>
                    <FormLabel>Name</FormLabel>
                    <Input
                      type="text"
                      placeholder="Enter your name"
                      {...register('name', { required: true })}
                      variant="filled"
                      focusBorderColor="teal.500"
                    />
                  </FormControl>
                )}
                <FormControl id="email" isRequired>
                  <FormLabel>Email</FormLabel>
                  <Input
                    type="email"
                    placeholder="Enter your email"
                    {...register('email', { required: true })}
                    variant="filled"
                    focusBorderColor="teal.500"
                  />
                </FormControl>
                <FormControl id="password" isRequired>
                  <FormLabel>Password</FormLabel>
                  <Input
                    type="password"
                    placeholder="Enter your password"
                    {...register('password', { required: true })}
                    variant="filled"
                    focusBorderColor="teal.500"
                  />
                </FormControl>
                <Button
                  type="submit"
                  colorScheme={isLogin ? 'teal' : 'blue'}
                  width="full"
                  size="lg"
                  mt={4}
                  borderRadius="md"
                >
                  {isLogin ? 'Login' : 'Register'}
                </Button>
              </VStack>
            </form>
            <HStack justify="center" mt={4}>
              <Button variant="link" colorScheme="teal" onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? 'Need to register?' : 'Already have an account?'}
              </Button>
            </HStack>
          </Box>
        </Box>
      </Container>
    </ChakraProvider>
  );
}

