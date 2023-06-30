import './App.css';
import { BrowserRouter as Router } from 'react-router-dom';

import AnimatedRoutes from './Components/AnimatedRoutes/AnimatedRoutes';

function App() {
  return (
      <Router>
        <AnimatedRoutes/>
      </Router>
  );
}

export default App;
