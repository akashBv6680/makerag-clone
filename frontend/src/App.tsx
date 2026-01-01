import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Upload from './pages/Upload';
import Search from './pages/Search';
import AIChat from './pages/AIChat';
import Chatbot from './pages/Chatbot';
import APIKeys from './pages/APIKeys';
import APIDocs from './pages/APIDocs';
import Settings from './pages/Settings';
import './App.css';

interface Project {
  id: string;
  name: string;
  docs: number;
  vectors: number;
}

function App() {
  const [currentProject, setCurrentProject] = useState<Project>({
    id: '1',
    name: 'DEMO APP',
    docs: 0,
    vectors: 0
  });
  const [projects, setProjects] = useState<Project[]>([currentProject]);
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    // Load user from localStorage
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  return (
    <Router>
      <div className="app-container">
        <Sidebar currentProject={currentProject} onProjectChange={setCurrentProject} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Upload project={currentProject} />} />
            <Route path="/search" element={<Search project={currentProject} />} />
            <Route path="/chat" element={<AIChat project={currentProject} />} />
            <Route path="/chatbot" element={<Chatbot project={currentProject} />} />
            <Route path="/keys" element={<APIKeys project={currentProject} />} />
            <Route path="/docs" element={<APIDocs />} />
            <Route path="/settings" element={<Settings project={currentProject} onProjectUpdate={setCurrentProject} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
