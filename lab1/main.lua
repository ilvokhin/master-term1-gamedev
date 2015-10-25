--- Simple balls physics. Based on Codingale LOVE examples:
--- https://github.com/Codingale/LOVE and official LOVE documentation.

debug = true
meter = 32
radius = 16
speed = 500
ballRestrinction = 0.5
edgeRestrinction = 0.6
math.randomseed(os.time())

function math.dist(x1, y1, x2, y2) return ((x2 - x1)^2+(y2 - y1)^2)^0.5 end

function addEdge(key, startX, startY, endX, endY)
  local edgeBody = love.physics.newBody(world, 0, 0, 'static')
  local edgeShape = love.physics.newEdgeShape(startX, startY, endX, endY)
  local edgeFixture = love.physics.newFixture(edgeBody, edgeShape)
  edgeFixture:setUserData(key)
  edgeFixture:setRestitution(edgeRestrinction)
  ---
  edgeBodies[key] = edgeBody
  edgeShapes[key] = edgeShape
  edgeFixtures[key] = edgeFixture
end

function addBall(x_pos, y_pos)
  local ballBody = love.physics.newBody(world, x_pos, y_pos, 'dynamic')
  local ballShape = love.physics.newCircleShape(0, 0, radius)
  local ballFixture = love.physics.newFixture(ballBody, ballShape)
  ballBody:setMassData(0, 0, 1, 0)
  ballFixture:setRestitution(ballRestrinction)
  ---
  ballBodies[#ballBodies + 1] = ballBody
  ballShapes[#ballShapes + 1] = ballShape
  ballFixtures[#ballFixtures + 1] = ballFixtures
  ballColors[#ballColors + 1] = {
    math.random(0, 255),
    math.random(0, 255),
    math.random(0, 255), 
    255
  }
end

function love.load()
  love.window.setTitle('Simple balls physics')
  love.graphics.setBackgroundColor(171, 235, 239)
  --- setup physics
  love.physics.setMeter(meter)
  world = love.physics.newWorld(0, 0, true)
  --- add border rectangles
  edgeBodies = {}
  edgeShapes = {}
  edgeFixtures = {}
  addEdge('up', 10, 10, 790, 10)
  addEdge('right', 790, 10, 790, 590)
  addEdge('down', 10, 590, 790, 590)
  addEdge('left', 10, 10, 10, 590)
  ---
  ballBodies = {}
  ballShapes = {}
  ballFixtures = {}
  ballColors = {}
  pickOut = {}
end

function love.keypressed(k)
  if k == " " then
    local randomY = math.random(-1000, 0)
    for k, v in pairs(ballBodies) do
      local body = ballBodies[k]
      body:applyLinearImpulse(0, randomY)
    end
  end
end

function love.mousepressed(x, y, button)
  if button == 'l' then
    local foundBall = -1
    for k, v in pairs(ballBodies) do
      local body = ballBodies[k]
      local shape = ballShapes[k]
      if math.dist(body:getX(), body:getY(), x, y) < shape:getRadius() then
        foundBall = k
        break
      end
    end
    if foundBall ~= -1 then
      pickOut[foundBall] = foundBall
    else
      addBall(x, y)
    end
  elseif button == 'r' then
    for k, v in pairs(pickOut) do
      local body = ballBodies[k]
      local ix = (x - body:getX())
      local iy = (y - body:getY())
      local dir = math.atan2(iy, ix)
      local dx, dy = speed * math.cos(dir), speed * math.sin(dir)
      body:applyLinearImpulse(dx, dy)
      body:setLinearDamping(0.25)
    end
    pickOut = {}
  end
end

function love.update(dt)
  world:update(dt)
end

function love.draw(dt)
  --- draw border rectangles
  local rectangles = {'up', 'right', 'down', 'left'}
  love.graphics.setColor(255, 255, 255)
  for k, v in pairs(rectangles) do
    local body = edgeBodies[v]
    local shape = edgeShapes[v]
    love.graphics.line(body:getWorldPoints(shape:getPoints()))
  end
  --- draw balls
  for k, v in pairs(ballBodies) do
    local body = ballBodies[k]
    local shape = ballShapes[k]
    local color = ballColors[k]
    love.graphics.setColor(0, 0, 0)
    love.graphics.circle('line', body:getX(), body:getY(), shape:getRadius())
    if pickOut[k] ~= nil then
      color = {255, 255, 255, 255}
    end
    love.graphics.setColor(color)
    love.graphics.circle('fill', body:getX(), body:getY(), shape:getRadius())
  end
end
