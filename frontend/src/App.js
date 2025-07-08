// Import React and a special function called `useState`
// React is the library that helps us build web components
// `useState` lets us store values that can change over time (like tab selection)
import React, { useState } from 'react';

// Import components from the Bootstrap UI library
// These are pre-styled buttons, dropdowns, layout tools, and tabs
import { Container, Row, Col, Button, Dropdown, Tabs, Tab } from 'react-bootstrap';

// Define our main App component (this is what gets displayed in the browser)
function App() {
  // Create a state variable called `activeTab` and a function to update it: `setActiveTab`
  // It starts with 'tab1' as the default selected tab
  const [activeTab, setActiveTab] = useState('tab1');

  // A function to simulate downloading data
  // When a user clicks a button or selects from a dropdown, this function is called
  const handleDownload = (type) => {
    // This shows a simple message on screen saying what is being "downloaded"
    alert(`Downloading ${type} data...`);
    // In a real app, you would connect this to a backend or file download logic
  };

  // Return the user interface — the HTML-like structure that React renders
  return (
    // `Container` gives a margin around the content (from Bootstrap)
    <Container className="mt-5">
      {/* Heading for the dashboard */}
      <h1 className="text-center text-primary mb-4">📊 Cappy AI Data Dashboard</h1>

      {/* Tabs let users switch between different data sections */}
      <Tabs
        id="data-tabs"                // Unique ID for this Tabs component
        activeKey={activeTab}         // Tells Tabs which one is currently selected
        onSelect={(k) => setActiveTab(k)} // Updates state when user clicks another tab
        className="mb-4"              // Bootstrap class: margin bottom
        justify                      // Makes the tabs stretch evenly across the page
      >

        {/* First tab: Customer Data */}
        <Tab eventKey="tab1" title="Customer Data">
          <Row className="mb-3">
            <Col>
              {/* A dropdown to choose between report types */}
              <Dropdown>
                {/* Button that toggles the dropdown menu */}
                <Dropdown.Toggle variant="info">Select Report Type</Dropdown.Toggle>

                {/* The menu that opens on click */}
                <Dropdown.Menu>
                  {/* Each option calls the handleDownload function with a different argument */}
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

          {/* A button below the dropdown to download customer data */}
          <Button variant="success" onClick={() => handleDownload('Customer')}>
            Download
          </Button>
        </Tab>

        {/* Second tab: Transaction Data */}
        <Tab eventKey="tab2" title="Transaction Data">
          <Row className="mb-3">
            <Col>
              {/* Dropdown for choosing download format */}
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

          {/* Button to download transaction data */}
          <Button variant="primary" onClick={() => handleDownload('Transaction')}>
            Download Transaction Data
          </Button>
        </Tab>

        {/* Third tab: Analytics */}
        <Tab eventKey="tab3" title="Analytics">
          {/* Informational text */}
          <p>This section can be extended for charts, insights, or uploads.</p>

          {/* Button to "export" analytics data */}
          <Button variant="dark" onClick={() => handleDownload('Analytics')}>
            Export Analytics
          </Button>
        </Tab>
      </Tabs>
    </Container>
  );
}

// Export this App component so it can be used in index.js to render in browser
export default App;
