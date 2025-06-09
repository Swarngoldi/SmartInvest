const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const cookieParser = require('cookie-parser');

const app = express();

// Enhanced CORS configuration
app.use(cors({
  origin: 'http://localhost:5173',
  credentials: true,
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With', 'X-Force-Generation'],
  exposedHeaders: ['Set-Cookie']
}));

app.use(express.json());
app.use(cookieParser());

// Global cache control middleware
app.use((req, res, next) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  next();
});

// Simple in-memory user database
const users = {
  'test@example.com': {
    password: 'test123',
    token: 'demo-auth-token'
  }
};

// Track generation attempts
let generationCounter = 0;

// Enhanced login endpoint
app.post('/login', (req, res) => {
  const { email, password } = req.body;
  
  if (users[email] && users[email].password === password) {
    res.cookie('authToken', users[email].token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      path: '/',
      domain: 'localhost',
      maxAge: 86400000
    });
    return res.json({ 
      success: true,
      message: 'Login successful'
    });
  }
  
  // Clear invalid login attempts
  res.clearCookie('authToken', {
    path: '/',
    domain: 'localhost'
  });
  res.status(401).json({ 
    error: 'Invalid credentials',
    solution: 'Check your email and password'
  });
});

// Enhanced authentication middleware
const authenticate = (req, res, next) => {
  const token = req.cookies.authToken;
  
  if (!token) {
    console.log('No auth token found');
    return res.status(401).json({ 
      message: 'Authentication required',
      solution: 'Please login first'
    });
  }

  if (token === 'demo-auth-token') {
    return next();
  }

  console.log('Invalid token received:', token);
  res.clearCookie('authToken', {
    path: '/',
    domain: 'localhost'
  });
  return res.status(401).json({ 
    message: 'Invalid session',
    solution: 'Please login again'
  });
};

// Atomic file operations
const atomicFileWrite = (filePath, data) => {
  return new Promise((resolve, reject) => {
    const tempPath = filePath + '.tmp';
    fs.writeFile(tempPath, JSON.stringify(data), (err) => {
      if (err) return reject(err);
      fs.rename(tempPath, filePath, (err) => {
        if (err) return reject(err);
        resolve();
      });
    });
  });
};

// Enhanced generate endpoint
app.post('/generate', authenticate, async (req, res) => {
  const { investment, risk } = req.body;
  const forceNew = req.query.force_new === 'true' || req.headers['x-force-generation'] === 'true';

  // Validate input
  const investmentAmount = parseFloat(investment);
  if (isNaN(investmentAmount)) {
    return res.status(400).json({ error: 'Investment must be a number' });
  }
  if (investmentAmount <= 0) {
    return res.status(400).json({ error: 'Investment must be positive' });
  }

  if (!['low', 'medium', 'high'].includes(risk)) {
    return res.status(400).json({ 
      error: 'Invalid risk level',
      validOptions: ['low', 'medium', 'high']
    });
  }

  console.log(`Starting generation for ₹${investmentAmount} with ${risk} risk (forceNew: ${forceNew})`);

  try {
    const pythonScript = path.join(__dirname, 'basket_generator.py');
    const outputFile = path.join(__dirname, `baskets_${Date.now()}.json`);
    const finalFile = path.join(__dirname, 'baskets.json');
    
    // Clear previous baskets if forceNew is true
    if (forceNew) {
      try {
        await fs.promises.writeFile(finalFile, JSON.stringify([]));
        console.log('Cleared previous baskets due to forceNew flag');
      } catch (clearError) {
        console.error('Error clearing previous baskets:', clearError);
      }
    }

    const command = `python ${pythonScript} ${investmentAmount} ${risk} ${outputFile}`;
    
    console.log(`Executing: ${command}`);

    // Execute Python script
    const { stdout, stderr } = await new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) {
          console.error('Generation failed:', {
            errorCode: error.code,
            signal: error.signal,
            stderr: stderr.trim()
          });
          return reject(new Error(stderr.trim() || 'Basket generation failed'));
        }
        resolve({ stdout, stderr });
      });
    });

    console.log('Python script output:', stdout.trim());

    // Verify and process the generated file
    const data = await fs.promises.readFile(outputFile, 'utf8');
    const baskets = JSON.parse(data);

    // Validate the generated data
    if (!Array.isArray(baskets)) {
      throw new Error('Invalid basket data format');
    }

    // Add generation metadata
    const enhancedBaskets = baskets.map(basket => ({
      ...basket,
      generationId: ++generationCounter,
      timestamp: new Date().toISOString()
    }));

    // Atomic write to final file
    await atomicFileWrite(finalFile, enhancedBaskets);

    console.log(`Successfully generated ${enhancedBaskets.length} baskets (GenID: ${generationCounter})`);
    
    // Clean up temp file
    fs.unlink(outputFile, () => {});

    res.json({
      baskets: enhancedBaskets,
      generationId: generationCounter,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('Generation error:', error);
    res.status(500).json({ 
      error: error.message || 'Basket generation failed',
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
});

// Enhanced baskets endpoint
app.get('/baskets', authenticate, async (req, res) => {
  console.log('Fetching baskets...');
  
  try {
    const filePath = path.join(__dirname, 'baskets.json');
    const data = await fs.promises.readFile(filePath, 'utf8');
    const baskets = JSON.parse(data);
    
    console.log(`Returning ${baskets.length} baskets (Latest GenID: ${generationCounter})`);
    
    res.json({
      baskets,
      generationId: generationCounter,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    if (error.code === 'ENOENT') {
      console.log('No baskets file found, returning empty array');
      return res.json({
        baskets: [],
        generationId: generationCounter,
        timestamp: new Date().toISOString()
      });
    }
    
    console.error('Baskets read error:', error);
    res.status(500).json({ 
      error: 'Failed to read baskets',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
});

// Enhanced health check
app.get('/health', (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: process.memoryUsage(),
    generationCount: generationCounter,
    dbConnection: true
  };
  res.json(health);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', {
    error: err.message,
    stack: err.stack,
    url: req.originalUrl,
    method: req.method
  });
  res.status(500).json({ 
    error: 'Internal server error',
    ...(process.env.NODE_ENV === 'development' && { details: err.stack })
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`\nServer running on http://localhost:${PORT}`);
  console.log('\nAvailable Endpoints:');
  console.log('POST /login        - Authenticate user');
  console.log('POST /generate     - Generate new baskets');
  console.log('GET /baskets       - Get current baskets');
  console.log('GET /health        - Server health check\n');
  console.log('Note: Ensure proper file permissions for baskets.json\n');
});