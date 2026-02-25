// Music Practice SRS - Client-Side JavaScript
// Uses browser localStorage for data persistence

// ============================================================================
// CONSTANTS
// ============================================================================

const STEPS_PER_DOUBLING = 16;
const HEADROOM_STEPS = 4;

const NodeType = {
    PIECE: 'piece',
    SEGMENT: 'segment',
    HOT_SPOT: 'hot_spot'
};

const Rating = {
    EASY: 'easy',
    GOOD: 'good',
    HARD: 'hard',
    AGAIN: 'again'
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function generateId() {
    return 'node_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function stepToMultiplier(step) {
    return Math.pow(2, step / STEPS_PER_DOUBLING);
}

function stepToBpm(step, targetBpm) {
    return Math.round(targetBpm * stepToMultiplier(step) * 10) / 10;
}

function stepToPercent(step) {
    const multiplier = stepToMultiplier(step);
    return Math.round((multiplier - 1) * 100 * 10) / 10;
}

function calculateStepDifference(previousStep, currentStep) {
    const diff = currentStep - previousStep;
    if (diff >= 1) return Rating.EASY;
    if (diff === 0) return Rating.GOOD;
    if (diff === -1) return Rating.HARD;
    return Rating.AGAIN;
}

// ============================================================================
// DATA STORAGE (localStorage)
// ============================================================================

class LocalStorage {
    static getNodes() {
        const data = localStorage.getItem('practice_nodes');
        return data ? JSON.parse(data) : [];
    }

    static saveNodes(nodes) {
        localStorage.setItem('practice_nodes', JSON.stringify(nodes));
    }

    static getSessions() {
        const data = localStorage.getItem('practice_sessions');
        return data ? JSON.parse(data) : [];
    }

    static saveSessions(sessions) {
        localStorage.setItem('practice_sessions', JSON.stringify(sessions));
    }

    static getNode(id) {
        const nodes = this.getNodes();
        return nodes.find(n => n.id === id);
    }

    static saveNode(node) {
        const nodes = this.getNodes();
        const index = nodes.findIndex(n => n.id === node.id);
        if (index >= 0) {
            nodes[index] = node;
        } else {
            nodes.push(node);
        }
        this.saveNodes(nodes);
    }

    static saveSession(session) {
        const sessions = this.getSessions();
        sessions.push(session);
        this.saveSessions(sessions);
    }

    static getDueNodes() {
        const nodes = this.getNodes();
        const now = new Date();
        return nodes
            .filter(n => new Date(n.srs.dueDate) <= now)
            .sort((a, b) => new Date(a.srs.dueDate) - new Date(b.srs.dueDate));
    }
}

// ============================================================================
// SRS FUNCTIONS
// ============================================================================

function updateSRSSchedule(srs, rating, isFirstAttempt = false) {
    srs.lastReviewed = new Date().toISOString();
    
    if (isFirstAttempt) {
        srs.interval = 1;
        srs.repetitions = 1;
        srs.easeFactor = 2.5;
        srs.dueDate = new Date(Date.now() + 86400000).toISOString(); // +1 day
        return;
    }
    
    if (rating === Rating.AGAIN) {
        srs.repetitions = 0;
        srs.interval = 1;
        srs.dueDate = new Date(Date.now() + 86400000).toISOString();
    } else {
        srs.repetitions += 1;
        
        if (rating === Rating.HARD) {
            srs.easeFactor = Math.max(1.3, srs.easeFactor - 0.15);
        } else if (rating === Rating.EASY) {
            srs.easeFactor = srs.easeFactor + 0.15;
        }
        
        if (srs.repetitions === 1) {
            srs.interval = 1;
        } else if (srs.repetitions === 2) {
            srs.interval = 6;
        } else {
            srs.interval = Math.round(srs.interval * srs.easeFactor);
        }
        
        srs.dueDate = new Date(Date.now() + srs.interval * 86400000).toISOString();
    }
}

// ============================================================================
// NODE CREATION
// ============================================================================

function createPracticeNode(type, title, measureStart, measureEnd, targetTempo, parentId = null) {
    return {
        id: generateId(),
        nodeType: type,
        title: title,
        measureStart: measureStart,
        measureEnd: measureEnd,
        targetTempoBpm: targetTempo,
        currentStep: 0,
        parentId: parentId,
        childrenIds: [],
        srs: {
            interval: 1,
            repetitions: 0,
            easeFactor: 2.5,
            dueDate: new Date().toISOString(),
            lastReviewed: null
        },
        hotSpotMeasure: null,
        hotSpotNotes: '',
        practiceHistory: [],
        createdAt: new Date().toISOString()
    };
}

function createHotSpotAndChildren(parentNode, hotSpotMeasure, hotSpotStep, notes = '') {
    console.log('=== Creating Hot Spot and Children ===');
    console.log('Parent:', parentNode.title, parentNode.id);
    console.log('Hot Spot Measure:', hotSpotMeasure);
    console.log('Hot Spot Step:', hotSpotStep);
    
    // Create hot spot
    const hotSpot = createPracticeNode(
        NodeType.HOT_SPOT,
        `${parentNode.title} - m.${hotSpotMeasure}`,
        hotSpotMeasure,
        hotSpotMeasure,
        parentNode.targetTempoBpm,
        parentNode.id
    );
    hotSpot.currentStep = hotSpotStep;
    hotSpot.hotSpotMeasure = hotSpotMeasure;
    hotSpot.hotSpotNotes = notes;
    updateSRSSchedule(hotSpot.srs, Rating.EASY, true);
    console.log('Created Hot Spot:', hotSpot.id, hotSpot.title, 'Due:', hotSpot.srs.dueDate);
    
    // Create before segment
    let beforeEnd;
    try {
        beforeEnd = String(parseInt(hotSpotMeasure) + 1);
    } catch {
        beforeEnd = `${hotSpotMeasure}+1`;
    }
    
    const beforeSegment = createPracticeNode(
        NodeType.SEGMENT,
        `${parentNode.title} - mm.${parentNode.measureStart}-${beforeEnd}`,
        parentNode.measureStart,
        beforeEnd,
        parentNode.targetTempoBpm,
        parentNode.id
    );
    updateSRSSchedule(beforeSegment.srs, Rating.EASY, true);
    console.log('Created Before Segment:', beforeSegment.id, beforeSegment.title, 'Due:', beforeSegment.srs.dueDate);
    
    // Create after segment
    const afterSegment = createPracticeNode(
        NodeType.SEGMENT,
        `${parentNode.title} - mm.${hotSpotMeasure}-${parentNode.measureEnd}`,
        hotSpotMeasure,
        parentNode.measureEnd,
        parentNode.targetTempoBpm,
        parentNode.id
    );
    updateSRSSchedule(afterSegment.srs, Rating.EASY, true);
    console.log('Created After Segment:', afterSegment.id, afterSegment.title, 'Due:', afterSegment.srs.dueDate);
    
    // Update parent
    parentNode.childrenIds = [hotSpot.id, beforeSegment.id, afterSegment.id];
    
    // Save all
    LocalStorage.saveNode(hotSpot);
    LocalStorage.saveNode(beforeSegment);
    LocalStorage.saveNode(afterSegment);
    LocalStorage.saveNode(parentNode);
    
    console.log('All nodes saved. Parent now has', parentNode.childrenIds.length, 'children');
    console.log('=== End Hot Spot Creation ===');
    
    return { hotSpot, beforeSegment, afterSegment };
}

// ============================================================================
// UI STATE
// ============================================================================

let currentScreen = 'main-menu';
let currentPracticeNode = null;
let practiceState = null;
let tempoMode = 'calculated'; // or 'quantized'

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.add('hidden'));
    document.getElementById('main-menu').style.display = 'none';
    
    if (screenId === 'main-menu') {
        document.getElementById('main-menu').style.display = 'block';
        updateStats();
    } else {
        document.getElementById(screenId).classList.remove('hidden');
    }
    
    currentScreen = screenId;
    
    // Load content for specific screens
    if (screenId === 'queue-screen') loadQueue();
    if (screenId === 'library-screen') loadLibrary('all');
}

function updateStats() {
    const nodes = LocalStorage.getNodes();
    const pieces = nodes.filter(n => n.nodeType === NodeType.PIECE).length;
    const segments = nodes.filter(n => n.nodeType === NodeType.SEGMENT).length;
    const hotSpots = nodes.filter(n => n.nodeType === NodeType.HOT_SPOT).length;
    const due = LocalStorage.getDueNodes().length;
    
    document.getElementById('stat-pieces').textContent = pieces;
    document.getElementById('stat-segments').textContent = segments;
    document.getElementById('stat-hotspots').textContent = hotSpots;
    document.getElementById('stat-due').textContent = due;
}

// ============================================================================
// ADD NEW PIECE
// ============================================================================

function addNewPiece() {
    const title = document.getElementById('new-piece-title').value.trim();
    const start = document.getElementById('new-piece-start').value.trim() || '1';
    const end = document.getElementById('new-piece-end').value.trim() || '100';
    const tempo = parseFloat(document.getElementById('new-piece-tempo').value);
    
    if (!title) {
        alert('Please enter a title');
        return;
    }
    
    if (!tempo || tempo < 30 || tempo > 240) {
        alert('Please enter a valid tempo (30-240 BPM)');
        return;
    }
    
    const piece = createPracticeNode(NodeType.PIECE, title, start, end, tempo);
    LocalStorage.saveNode(piece);
    
    // Clear form
    document.getElementById('new-piece-title').value = '';
    document.getElementById('new-piece-start').value = '1';
    document.getElementById('new-piece-end').value = '100';
    document.getElementById('new-piece-tempo').value = '120';
    
    showScreen('main-menu');
}

// ============================================================================
// QUEUE & LIBRARY
// ============================================================================

function loadQueue() {
    const due = LocalStorage.getDueNodes();
    const container = document.getElementById('queue-list');
    
    if (due.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🎉</div><p>Nothing due! All caught up.</p></div>';
        return;
    }
    
    container.innerHTML = due.map((node, i) => {
        const now = new Date();
        const dueDate = new Date(node.srs.dueDate);
        const daysOverdue = Math.floor((now - dueDate) / 86400000);
        const overdueClass = daysOverdue > 0 ? 'overdue' : '';
        
        return `
            <div class="queue-item">
                <h4>${i + 1}. ${node.title}</h4>
                <div class="item-details">
                    <div class="item-detail">
                        <span class="item-detail-label">Type</span>
                        <span class="item-detail-value">${node.nodeType}</span>
                    </div>
                    <div class="item-detail">
                        <span class="item-detail-label">Measures</span>
                        <span class="item-detail-value">${node.measureStart}-${node.measureEnd}</span>
                    </div>
                    <div class="item-detail">
                        <span class="item-detail-label">Current Tempo</span>
                        <span class="item-detail-value">${stepToBpm(node.currentStep, node.targetTempoBpm)} BPM</span>
                    </div>
                    <div class="item-detail">
                        <span class="item-detail-label">Due</span>
                        <span class="item-detail-value ${overdueClass}">
                            ${daysOverdue > 0 ? `${daysOverdue} days overdue` : 'Today'}
                        </span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function loadLibrary(filter) {
    const nodes = LocalStorage.getNodes();
    let filtered = nodes;
    
    if (filter === 'pieces') filtered = nodes.filter(n => n.nodeType === NodeType.PIECE);
    if (filter === 'segments') filtered = nodes.filter(n => n.nodeType === NodeType.SEGMENT);
    if (filter === 'hotspots') filtered = nodes.filter(n => n.nodeType === NodeType.HOT_SPOT);
    
    const container = document.getElementById('library-list');
    
    if (filtered.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No items in library yet.</p></div>';
        return;
    }
    
    container.innerHTML = filtered.map(node => {
        const now = new Date();
        const dueDate = new Date(node.srs.dueDate);
        const isDue = dueDate <= now;
        const daysUntilDue = Math.ceil((dueDate - now) / 86400000);
        
        let dueText;
        let dueClass = '';
        
        if (isDue) {
            const daysOverdue = Math.abs(daysUntilDue);
            if (daysOverdue === 0) {
                dueText = 'Due today';
                dueClass = 'due-soon';
            } else {
                dueText = `${daysOverdue} day${daysOverdue === 1 ? '' : 's'} overdue`;
                dueClass = 'overdue';
            }
        } else {
            dueText = `Due in ${daysUntilDue} day${daysUntilDue === 1 ? '' : 's'}`;
        }
        
        const dueDateFormatted = dueDate.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric',
            year: dueDate.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
        });
        
        return `
        <div class="library-item">
            <h4>${node.title}</h4>
            <div class="item-details">
                <div class="item-detail">
                    <span class="item-detail-label">Type</span>
                    <span class="item-detail-value">${node.nodeType}</span>
                </div>
                <div class="item-detail">
                    <span class="item-detail-label">Measures</span>
                    <span class="item-detail-value">${node.measureStart}-${node.measureEnd}</span>
                </div>
                <div class="item-detail">
                    <span class="item-detail-label">Target</span>
                    <span class="item-detail-value">${node.targetTempoBpm} BPM</span>
                </div>
                <div class="item-detail">
                    <span class="item-detail-label">Current</span>
                    <span class="item-detail-value">${stepToBpm(node.currentStep, node.targetTempoBpm)} BPM</span>
                </div>
                <div class="item-detail">
                    <span class="item-detail-label">Due Date</span>
                    <span class="item-detail-value ${dueClass}">${dueDateFormatted}</span>
                </div>
                <div class="item-detail">
                    <span class="item-detail-label">Status</span>
                    <span class="item-detail-value ${dueClass}">${dueText}</span>
                </div>
                <div class="item-detail">
                    <span class="item-detail-label">Sessions</span>
                    <span class="item-detail-value">${node.practiceHistory.length}</span>
                </div>
                <div class="item-detail">
                    <span class="item-detail-label">Interval</span>
                    <span class="item-detail-value">${node.srs.interval} day${node.srs.interval === 1 ? '' : 's'}</span>
                </div>
            </div>
        </div>
    `;
    }).join('');
}

function showLibraryTab(filter) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    loadLibrary(filter);
}

// ============================================================================
// PRACTICE SESSION
// ============================================================================

function startPractice() {
    const due = LocalStorage.getDueNodes();
    if (due.length === 0) {
        alert('Nothing due to practice!');
        return;
    }
    
    currentPracticeNode = due[0];
    initializePracticeSession(currentPracticeNode);
}

function initializePracticeSession(node) {
    practiceState = {
        nodeId: node.id,
        currentStep: HEADROOM_STEPS,
        currentMeasure: node.measureStart,
        hotSpotMeasure: null,
        lastSuccessfulStep: null,
        achievedStep: null,
        hotSpotDiscovered: false,
        searchPhase: 'initial',
        searchPattern: [],
        patternIndex: 0,
        history: []
    };
    
    // Show practice screen
    showScreen('practice-screen');
    
    // Update header
    document.getElementById('practice-title').textContent = node.title;
    document.getElementById('practice-type').textContent = node.nodeType;
    document.getElementById('practice-measures').textContent = `mm.${node.measureStart}-${node.measureEnd}`;
    document.getElementById('practice-target-tempo').textContent = `${node.targetTempoBpm} BPM`;
    
    // Clear history
    document.getElementById('practice-history').innerHTML = '';
    
    // Update display
    updatePracticeDisplay();
}

function updatePracticeDisplay() {
    const node = currentPracticeNode;
    const state = practiceState;
    const tempo = stepToBpm(state.currentStep, node.targetTempoBpm);
    
    document.getElementById('practice-current-tempo').textContent = `${tempo} BPM`;
    document.getElementById('practice-step').innerHTML = 
        `${state.currentStep >= 0 ? '+' : ''}${state.currentStep}<br><span style="font-size: 0.6em; opacity: 0.8;">${stepToPercent(state.currentStep) >= 0 ? '+' : ''}${stepToPercent(state.currentStep)}%</span>`;
    document.getElementById('current-measure').textContent = state.currentMeasure;
    document.getElementById('error-measure-input').value = '';
}

function handlePracticeResponse() {
    const errorMeasure = document.getElementById('error-measure-input').value.trim();
    const success = errorMeasure === '';
    
    // Add to history
    addPracticeHistory(success, errorMeasure);
    
    // Process based on search phase
    if (practiceState.searchPhase === 'initial') {
        handleInitialPhase(success, errorMeasure);
    } else if (practiceState.searchPhase === 'after_first_drop') {
        handleAfterFirstDrop(success, errorMeasure);
    } else if (practiceState.searchPhase === 'downward') {
        handleDownwardSearch(success, errorMeasure);
    } else if (practiceState.searchPhase === 'upward') {
        handleUpwardSearch(success, errorMeasure);
    }
}

function addPracticeHistory(success, errorMeasure) {
    const tempo = stepToBpm(practiceState.currentStep, currentPracticeNode.targetTempoBpm);
    const percent = stepToPercent(practiceState.currentStep);
    
    const historyEl = document.getElementById('practice-history');
    const item = document.createElement('div');
    item.className = `history-item ${success ? 'success' : 'error'}`;
    item.textContent = success
        ? `Step ${practiceState.currentStep >= 0 ? '+' : ''}${practiceState.currentStep} (${tempo} BPM, ${percent >= 0 ? '+' : ''}${percent}%): ✓ From m.${practiceState.currentMeasure}`
        : `Step ${practiceState.currentStep >= 0 ? '+' : ''}${practiceState.currentStep} (${tempo} BPM, ${percent >= 0 ? '+' : ''}${percent}%): ✗ Error at m.${errorMeasure}`;
    
    historyEl.insertBefore(item, historyEl.firstChild);
}

function handleInitialPhase(success, errorMeasure) {
    if (success) {
        // Completed at +19%!
        practiceState.achievedStep = practiceState.currentStep;
        practiceState.hotSpotDiscovered = false;
        completeSession();
    } else {
        // Hit error - drop to -12
        practiceState.hotSpotMeasure = errorMeasure;
        practiceState.currentMeasure = errorMeasure;
        practiceState.currentStep -= 16;
        practiceState.searchPhase = 'after_first_drop';
        updatePracticeDisplay();
    }
}

function handleAfterFirstDrop(success, errorMeasure) {
    if (!success) {
        // Still failing - start downward search
        if (errorMeasure !== practiceState.hotSpotMeasure) {
            practiceState.hotSpotMeasure = errorMeasure;
            practiceState.currentMeasure = errorMeasure;
        }
        practiceState.searchPhase = 'downward';
        practiceState.searchPattern = [8, 4, 2, 1];
        practiceState.patternIndex = 0;
        continueDownwardSearch();
    } else {
        // Success - start upward search
        practiceState.lastSuccessfulStep = practiceState.currentStep;
        practiceState.searchPhase = 'upward';
        practiceState.searchPattern = [8, 4, 2, 1];
        practiceState.patternIndex = 0;
        continueUpwardSearch();
    }
}

function handleDownwardSearch(success, errorMeasure) {
    if (success) {
        practiceState.lastSuccessfulStep = practiceState.currentStep;
        practiceState.searchPhase = 'upward';
        practiceState.searchPattern = [4, 2, 1];
        practiceState.patternIndex = 0;
        continueUpwardSearch();
    } else {
        if (errorMeasure !== practiceState.hotSpotMeasure) {
            practiceState.hotSpotMeasure = errorMeasure;
            practiceState.currentMeasure = errorMeasure;
        }
        continueDownwardSearch();
    }
}

function handleUpwardSearch(success, errorMeasure) {
    if (success) {
        practiceState.lastSuccessfulStep = practiceState.currentStep;
    } else {
        if (errorMeasure !== practiceState.hotSpotMeasure) {
            practiceState.hotSpotMeasure = errorMeasure;
            practiceState.currentMeasure = errorMeasure;
        }
        practiceState.currentStep -= practiceState.searchPattern[practiceState.patternIndex - 1];
    }
    continueUpwardSearch();
}

function continueDownwardSearch() {
    if (practiceState.patternIndex < practiceState.searchPattern.length) {
        const dropAmount = practiceState.searchPattern[practiceState.patternIndex];
        practiceState.currentStep -= dropAmount;
        practiceState.patternIndex++;
        
        if (practiceState.currentStep < -27) {
            practiceState.achievedStep = practiceState.currentStep;
            practiceState.hotSpotDiscovered = true;
            completeSession();
            return;
        }
        
        updatePracticeDisplay();
    } else {
        practiceState.achievedStep = practiceState.currentStep;
        practiceState.hotSpotDiscovered = true;
        completeSession();
    }
}

function continueUpwardSearch() {
    if (practiceState.patternIndex < practiceState.searchPattern.length) {
        const raiseAmount = practiceState.searchPattern[practiceState.patternIndex];
        practiceState.currentStep += raiseAmount;
        practiceState.patternIndex++;
        updatePracticeDisplay();
    } else {
        practiceState.achievedStep = practiceState.lastSuccessfulStep;
        practiceState.hotSpotDiscovered = true;
        completeSession();
    }
}

function completeSession() {
    const node = currentPracticeNode;
    const state = practiceState;
    
    // Build summary
    const isFirstAttempt = node.srs.repetitions === 0;
    const previousStep = node.currentStep;
    const achievedStep = state.achievedStep;
    
    let rating;
    if (isFirstAttempt) {
        rating = Rating.EASY;
    } else {
        rating = calculateStepDifference(previousStep, achievedStep);
    }
    
    const tempo = stepToBpm(achievedStep, node.targetTempoBpm);
    const percent = stepToPercent(achievedStep);
    
    let summaryHTML = `
        <div class="summary-row">
            <span class="summary-label">Achieved Step:</span>
            <span class="summary-value highlight">${achievedStep >= 0 ? '+' : ''}${achievedStep}</span>
        </div>
        <div class="summary-row">
            <span class="summary-label">Tempo:</span>
            <span class="summary-value">${tempo} BPM (${percent >= 0 ? '+' : ''}${percent}%)</span>
        </div>
        <div class="summary-row">
            <span class="summary-label">Rating:</span>
            <span class="summary-value">${rating.toUpperCase()}</span>
        </div>
    `;
    
    if (!isFirstAttempt) {
        const stepDiff = achievedStep - previousStep;
        summaryHTML += `
            <div class="summary-row">
                <span class="summary-label">Change from Previous:</span>
                <span class="summary-value">${stepDiff >= 0 ? '+' : ''}${stepDiff} steps</span>
            </div>
        `;
    }
    
    document.getElementById('session-summary').innerHTML = summaryHTML;
    
    // Show hot spot input if discovered
    if (state.hotSpotDiscovered && state.hotSpotMeasure) {
        document.getElementById('hot-spot-input').classList.remove('hidden');
    } else {
        document.getElementById('hot-spot-input').classList.add('hidden');
    }
    
    // Save the session data for continueToNext
    sessionStorage.setItem('pendingSession', JSON.stringify({
        node: node,
        state: state,
        rating: rating,
        isFirstAttempt: isFirstAttempt
    }));
    
    // Show completion screen FIRST
    showScreen('session-complete-screen');
    
    // THEN calculate remaining due (this will be updated properly after save)
    // For now, just show the button - count will be accurate after they click it
    const continueBtn = document.getElementById('continue-practice-btn');
    continueBtn.textContent = 'Continue to Next';
    continueBtn.style.display = 'inline-block';
}

function continueToNext() {
    // Get the pending session data
    const pending = JSON.parse(sessionStorage.getItem('pendingSession'));
    if (!pending) {
        console.error('No pending session found');
        showScreen('main-menu');
        return;
    }
    
    // Save the session first
    savePendingSession();
    
    // NOW check for next node (after creating children)
    const nextDue = LocalStorage.getDueNodes();
    console.log('Due nodes after save:', nextDue.length);
    
    if (nextDue.length > 0) {
        currentPracticeNode = nextDue[0];
        initializePracticeSession(currentPracticeNode);
    } else {
        showScreen('main-menu');
    }
}

function saveAndExit() {
    // Save the session before returning to menu
    savePendingSession();
    showScreen('main-menu');
}

function savePendingSession() {
    const pending = sessionStorage.getItem('pendingSession');
    if (!pending) {
        console.log('No pending session to save');
        return;
    }
    
    const data = JSON.parse(pending);
    
    // IMPORTANT: Reload the node from storage to get fresh data
    const node = LocalStorage.getNode(data.node.id);
    if (!node) {
        console.error('Could not find node:', data.node.id);
        return;
    }
    
    const state = data.state;
    const rating = data.rating;
    const isFirstAttempt = data.isFirstAttempt;
    
    // Get hot spot notes if applicable
    const hotSpotNotes = state.hotSpotDiscovered && state.hotSpotMeasure
        ? document.getElementById('hot-spot-notes').value.trim()
        : '';
    
    // Create session record
    const session = {
        sessionId: generateId(),
        nodeId: node.id,
        timestamp: new Date().toISOString(),
        startingStep: HEADROOM_STEPS,
        achievedStep: state.achievedStep,
        rating: rating,
        hotSpotDiscovered: state.hotSpotDiscovered,
        hotSpotMeasure: state.hotSpotMeasure,
        notes: hotSpotNotes
    };
    
    // Update node
    node.currentStep = state.achievedStep;
    node.practiceHistory.push(session);
    updateSRSSchedule(node.srs, rating, isFirstAttempt);
    LocalStorage.saveNode(node);
    LocalStorage.saveSession(session);
    
    console.log('Session saved:', session);
    
    // Create children if hot spot discovered
    if (state.hotSpotDiscovered && state.hotSpotMeasure) {
        console.log('Creating hot spot and children for measure', state.hotSpotMeasure);
        const result = createHotSpotAndChildren(node, state.hotSpotMeasure, state.achievedStep, hotSpotNotes);
        console.log('Created children:', result);
    }
    
    sessionStorage.removeItem('pendingSession');
}

function toggleTempoMode() {
    tempoMode = tempoMode === 'calculated' ? 'quantized' : 'calculated';
    document.getElementById('tempo-mode-btn').textContent = 
        tempoMode === 'calculated' ? 'Switch to Quantized' : 'Switch to Calculated';
    // Note: Quantized mode would need the TEMPOS array - simplified for now
}

// ============================================================================
// DATA MANAGEMENT
// ============================================================================

function confirmClearData() {
    const nodes = LocalStorage.getNodes();
    const sessions = LocalStorage.getSessions();
    
    const message = `This will permanently delete:\n- ${nodes.length} practice nodes\n- ${sessions.length} practice sessions\n\nThis CANNOT be undone!\n\nAre you sure?`;
    
    if (confirm(message)) {
        if (confirm('Really delete everything? This is your last chance!')) {
            localStorage.removeItem('practice_nodes');
            localStorage.removeItem('practice_sessions');
            alert('All data cleared!');
            showScreen('main-menu');
        }
    }
}

function exportData() {
    const data = {
        nodes: LocalStorage.getNodes(),
        sessions: LocalStorage.getSessions(),
        exportDate: new Date().toISOString(),
        version: '1.0'
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `practice-data-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

function importAnkiData() {
    const fileInput = document.getElementById('anki-import-file');
    const statusDiv = document.getElementById('import-status');
    
    if (!fileInput.files || fileInput.files.length === 0) {
        statusDiv.textContent = '❌ Please select a file first';
        statusDiv.style.color = 'var(--error)';
        return;
    }
    
    const file = fileInput.files[0];
    const reader = new FileReader();
    
    reader.onload = function(e) {
        try {
            const ankiData = JSON.parse(e.target.result);
            const imported = convertAnkiToPracticeNodes(ankiData);
            
            statusDiv.innerHTML = `✓ Imported ${imported.nodes} nodes and ${imported.sessions} sessions`;
            statusDiv.style.color = 'var(--success)';
            
            updateStats();
        } catch (error) {
            statusDiv.textContent = `❌ Error: ${error.message}`;
            statusDiv.style.color = 'var(--error)';
        }
    };
    
    reader.readAsText(file);
}

function convertAnkiToPracticeNodes(ankiData) {
    /*
    Tim's Anki Structure:
    - One Note per piece/movement
    - Cards use Ahnentafel numbering:
      - Card 1 (Node 1): Root node (Start1 to End1)
      - Card 2 (HS1): Hot Spot 1 at measure HS1
      - Card 3 (Node 2): Left child (Start1 to End2, where End2 = HS1-1)
      - Card 4 (Node 3): Right child (Start3 to End1, where Start3 = HS1+1)
      - etc.
    
    Fields per node N:
    - StartN, EndN: measure range
    - TempoN: last successful tempo (as step)
    - HSN: hot spot measure number
    - HSTempoN: hot spot tempo
    - HSNotesN: notes about the hot spot
    */
    
    let nodesImported = 0;
    
    if (!ankiData.notes || !Array.isArray(ankiData.notes)) {
        throw new Error('Invalid Anki export format. Expected "notes" array.');
    }
    
    ankiData.notes.forEach(ankiNote => {
        const fields = ankiNote.fields || {};
        
        // Extract base info
        const instrument = fields.Instr || '';
        const title = fields.Title || 'Untitled';
        const fullTitle = instrument ? `${instrument} - ${title}` : title;
        
        // Get target tempo from the piece (use first node's target or default)
        // In your system, the target is implicit - we'll extract from the context
        // For now, use a reasonable default or try to infer from Tempo1
        const targetTempo = parseFloat(fields.TargetTempo) || 120;
        
        // Process each node in the Ahnentafel tree
        // We'll create nodes based on populated fields
        const nodes = [];
        
        // Node 1 (Card 1) - Root
        if (fields.Start1 && fields.End1) {
            const node1 = createPracticeNode(
                NodeType.PIECE,
                fullTitle,
                fields.Start1,
                fields.End1,
                targetTempo
            );
            
            // Set current step (Tempo1 is stored as step number)
            if (fields.Tempo1) {
                node1.currentStep = parseInt(fields.Tempo1) || 0;
            }
            
            // Import SRS data if available
            if (ankiNote.srsData) {
                node1.srs.dueDate = ankiNote.srsData.due || new Date().toISOString();
                node1.srs.interval = parseInt(ankiNote.srsData.interval) || 1;
                node1.srs.easeFactor = parseFloat(ankiNote.srsData.easeFactor) || 2.5;
                node1.srs.repetitions = parseInt(ankiNote.srsData.reps) || 0;
            }
            
            nodes.push({ node: node1, ankiNodeNum: 1, parentNum: null });
        }
        
        // Hot Spot 1 (Card 2)
        if (fields.HS1) {
            const hs1 = createPracticeNode(
                NodeType.HOT_SPOT,
                `${fullTitle} - m.${fields.HS1}`,
                fields.HS1,
                fields.HS1,
                targetTempo
            );
            
            // Set hot spot tempo
            if (fields.HSTempo1) {
                hs1.currentStep = parseInt(fields.HSTempo1) || 0;
            } else if (fields.Tempo1) {
                hs1.currentStep = parseInt(fields.Tempo1) || 0;
            }
            
            hs1.hotSpotMeasure = fields.HS1;
            hs1.hotSpotNotes = fields.HSNotes1 || '';
            
            nodes.push({ node: hs1, ankiNodeNum: 2, parentNum: 1 });
        }
        
        // Node 2 (Card 3) - Left child (Start1 to End2)
        if (fields.End2) {
            const node2 = createPracticeNode(
                NodeType.SEGMENT,
                `${fullTitle} - mm.${fields.Start1}-${fields.End2}`,
                fields.Start1,
                fields.End2,
                targetTempo
            );
            
            if (fields.Tempo2) {
                node2.currentStep = parseInt(fields.Tempo2) || 0;
            }
            
            nodes.push({ node: node2, ankiNodeNum: 3, parentNum: 1 });
        }
        
        // Node 3 (Card 4) - Right child (Start3 to End1)
        if (fields.Start3) {
            const node3 = createPracticeNode(
                NodeType.SEGMENT,
                `${fullTitle} - mm.${fields.Start3}-${fields.End1}`,
                fields.Start3,
                fields.End1,
                targetTempo
            );
            
            if (fields.Tempo3) {
                node3.currentStep = parseInt(fields.Tempo3) || 0;
            }
            
            nodes.push({ node: node3, ankiNodeNum: 4, parentNum: 1 });
        }
        
        // Process additional nodes (4-7, hot spots 2-3, etc.)
        // Following the same pattern for deeper levels
        
        // Hot Spot 2 (Card 5)
        if (fields.HS2) {
            const hs2 = createPracticeNode(
                NodeType.HOT_SPOT,
                `${fullTitle} - m.${fields.HS2}`,
                fields.HS2,
                fields.HS2,
                targetTempo
            );
            
            if (fields.HSTempo2) {
                hs2.currentStep = parseInt(fields.HSTempo2) || 0;
            } else if (fields.Tempo2) {
                hs2.currentStep = parseInt(fields.Tempo2) || 0;
            }
            
            hs2.hotSpotMeasure = fields.HS2;
            hs2.hotSpotNotes = fields.HSNotes2 || '';
            
            nodes.push({ node: hs2, ankiNodeNum: 5, parentNum: 3 });
        }
        
        // Hot Spot 3 (Card 6)
        if (fields.HS3) {
            const hs3 = createPracticeNode(
                NodeType.HOT_SPOT,
                `${fullTitle} - m.${fields.HS3}`,
                fields.HS3,
                fields.HS3,
                targetTempo
            );
            
            if (fields.HSTempo3) {
                hs3.currentStep = parseInt(fields.HSTempo3) || 0;
            } else if (fields.Tempo3) {
                hs3.currentStep = parseInt(fields.Tempo3) || 0;
            }
            
            hs3.hotSpotMeasure = fields.HS3;
            hs3.hotSpotNotes = fields.HSNotes3 || '';
            
            nodes.push({ node: hs3, ankiNodeNum: 6, parentNum: 4 });
        }
        
        // Now establish parent-child relationships using Ahnentafel numbers
        // In Ahnentafel: parent of node N is floor(N/2)
        const nodeMap = new Map();
        nodes.forEach(({ node, ankiNodeNum }) => {
            nodeMap.set(ankiNodeNum, node);
        });
        
        nodes.forEach(({ node, ankiNodeNum, parentNum }) => {
            const calculatedParentNum = Math.floor(ankiNodeNum / 2);
            const actualParentNum = parentNum || (ankiNodeNum > 1 ? calculatedParentNum : null);
            
            if (actualParentNum && nodeMap.has(actualParentNum)) {
                const parentNode = nodeMap.get(actualParentNum);
                node.parentId = parentNode.id;
                
                // Add to parent's children if not already there
                if (!parentNode.childrenIds.includes(node.id)) {
                    parentNode.childrenIds.push(node.id);
                }
            }
        });
        
        // Save all nodes
        nodes.forEach(({ node }) => {
            LocalStorage.saveNode(node);
            nodesImported++;
        });
    });
    
    return { nodes: nodesImported, sessions: 0 };
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    showScreen('main-menu');
});
