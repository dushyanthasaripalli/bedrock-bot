import React, { useState } from 'react';
import { Container, Row, Col, Button, Dropdown, Tabs, Tab } from 'react-bootstrap';

function App() {
  const [activeTab, setActiveTab] = useState('tab1');

  const handleDownload = (type) => {
    alert(`Downloading ${type} data...`);
    // TODO: Replace with real download logic
  };

  return (
    <Container className="mt-5">
      <h1 className="text-center text-primary mb-4">📊 Cappy AI Data Dashboard</h1>

      <Tabs
        id="data-tabs"
        activeKey={activeTab}
        onSelect={(k) => setActiveTab(k)}
        className="mb-4"
        justify
      >
        <Tab eventKey="tab1" title="Customer Data">
          <Row className="mb-3">
            <Col>
              <Dropdown>
                <Dropdown.Toggle variant="info">Select Report Type</Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item onClick={() => handleDownload('Customer Summary')}>
                    Customer Summary
                  </Dropdown.Item>
                  <Dropdown.Item onClick={() => handleDownload('Customer Full')}>
                    Customer Full
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Col>
          </Row>
          <Button variant="success" onClick={() => handleDownload('Customer')}>Download</Button>
        </Tab>

        <Tab eventKey="tab2" title="Transaction Data">
          <Row className="mb-3">
            <Col>
              <Dropdown>
                <Dropdown.Toggle variant="warning">Select Format</Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item onClick={() => handleDownload('CSV')}>
                    CSV
                  </Dropdown.Item>
                  <Dropdown.Item onClick={() => handleDownload('Excel')}>
                    Excel
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </Col>
          </Row>
          <Button variant="primary" onClick={() => handleDownload('Transaction')}>
            Download Transaction Data
          </Button>
        </Tab>

        <Tab eventKey="tab3" title="Analytics">
          <p>This section can be extended for charts, insights, or uploads.</p>
          <Button variant="dark" onClick={() => handleDownload('Analytics')}>
            Export Analytics
          </Button>
        </Tab>
      </Tabs>
    </Container>
  );
}

export default App;









// import React from 'react';

// function App() {
//   return (
//     <div>
//       <h1>Cappy AI Development!</h1>
//       <p>It's getting there....</p>
//     </div>
//   );
// }

// export default App;




// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
