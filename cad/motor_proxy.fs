FeatureScript 2200;
import(path : "onshape/std/geometry.fs", version : "2200.0");

// ============================================================================
//  GROUPED PER-MOTOR DATA TABLE
//  Each entry is ONE motor record with named fields. To add a motor, copy a
//  block and edit the values, then add its name to the MotorType enum below.
//  All lengths are in millimeters (* millimeter).
//
//    od              : outer diameter of the motor body cylinder
//    length          : axial length of the motor body cylinder
//    boltCircleOuter : bolt-circle DIAMETER on the FRONT 'output' face
//    nBoltsOuter     : number of bolts on the front face
//    boltCircleInner : bolt-circle DIAMETER on the BACK 'housing' face
//    nBoltsInner     : number of bolts on the back face
//    boltDia         : nominal clearance hole diameter for the bolts
// ============================================================================
const MOTORS = {
    "RS04" : {
        "od"              : 90  * millimeter,
        "length"          : 40  * millimeter,
        "boltCircleOuter" : 70  * millimeter,
        "nBoltsOuter"     : 6,
        "boltCircleInner" : 50  * millimeter,
        "nBoltsInner"     : 4,
        "boltDia"         : 4.5 * millimeter
    },
    "RS06" : {
        "od"              : 110 * millimeter,
        "length"          : 50  * millimeter,
        "boltCircleOuter" : 90  * millimeter,
        "nBoltsOuter"     : 8,
        "boltCircleInner" : 64  * millimeter,
        "nBoltsInner"     : 6,
        "boltDia"         : 5.5 * millimeter
    },
    "RS03" : {
        "od"              : 70  * millimeter,
        "length"          : 32  * millimeter,
        "boltCircleOuter" : 54  * millimeter,
        "nBoltsOuter"     : 6,
        "boltCircleInner" : 40  * millimeter,
        "nBoltsInner"     : 4,
        "boltDia"         : 3.4 * millimeter
    },
    "RS02" : {
        "od"              : 50  * millimeter,
        "length"          : 25  * millimeter,
        "boltCircleOuter" : 38  * millimeter,
        "nBoltsOuter"     : 4,
        "boltCircleInner" : 28  * millimeter,
        "nBoltsInner"     : 4,
        "boltDia"         : 2.7 * millimeter
    },
    "RS05" : {
        "od"              : 100 * millimeter,
        "length"          : 45  * millimeter,
        "boltCircleOuter" : 80  * millimeter,
        "nBoltsOuter"     : 8,
        "boltCircleInner" : 58  * millimeter,
        "nBoltsInner"     : 6,
        "boltDia"         : 5.5 * millimeter
    }
};

// Dropdown of motor keys. NOTE: enum constant names must EXACTLY match the
// string keys used in the MOTORS map above (toString(enumValue) -> "RS04").
export enum MotorType
{
    RS04,
    RS06,
    RS03,
    RS02,
    RS05
}

// ============================================================================
//  FEATURE
// ============================================================================
annotation { "Feature Type Name" : "Motor proxy" }
export const motorProxy = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Motor type" }
        definition.motorType is MotorType;

        annotation { "Name" : "Use custom placement" }
        definition.useOrigin is boolean;

        if (definition.useOrigin)
        {
            annotation { "Name" : "Placement vertex",
                         "Filter" : EntityType.VERTEX,
                         "MaxNumberOfPicks" : 1 }
            definition.origin is Query;
        }
    }
    {
        // Look up the grouped record for the chosen motor.
        const motor = MOTORS[toString(definition.motorType)];

        // Resolve the placement coordinate system. Default: world origin,
        // body axis along +Z; the back/housing face sits at the origin and
        // the front/output face is at z = length.
        var cSys = coordSystem(WORLD_ORIGIN, X_DIRECTION, Z_DIRECTION);
        if (definition.useOrigin && !isQueryEmpty(context, definition.origin))
        {
            const pt = evVertexPoint(context, { "vertex" : definition.origin });
            cSys = coordSystem(pt, X_DIRECTION, Z_DIRECTION);
        }

        buildMotor(context, id, motor, cSys);
    });

// ============================================================================
//  BUILDER  — given a motor record + placement, builds the proxy.
//  Adding a motor = adding one record above; this builder is generic.
// ============================================================================
function buildMotor(context is Context, id is Id, motor is map, cSys is CoordSystem)
{
    const od     = motor.od;
    const length = motor.length;
    const r      = od / 2;

    // ---- Body cylinder ------------------------------------------------------
    // Built along the placement Z axis, from z = 0 (back/housing face) to
    // z = length (front/output face). cSys.origin is the back-face center.
    const back  = cSys.origin;
    const front = back + cSys.zAxis * length;

    fCylinder(context, id + "body", {
            "topCenter"    : front,
            "bottomCenter" : back,
            "radius"       : r
    });

    // ---- Front 'output' face bolt holes ------------------------------------
    // Cut INWARD from the front face (at z = length) toward -Z.
    makeBoltRing(context, id + "outer", id + "body", cSys,
            motor.boltCircleOuter / 2,   // bolt-circle radius
            motor.nBoltsOuter,
            motor.boltDia / 2,           // hole radius
            length,                      // z of the front face plane
            -cSys.zAxis,                 // cut direction (into the body)
            length / 3);                 // cut depth

    // ---- Back 'housing' face bolt holes ------------------------------------
    // Cut INWARD from the back face (at z = 0) toward +Z.
    makeBoltRing(context, id + "inner", id + "body", cSys,
            motor.boltCircleInner / 2,
            motor.nBoltsInner,
            motor.boltDia / 2,
            0 * meter,                   // z of the back face plane
            cSys.zAxis,                  // cut direction (into the body)
            length / 3);                 // cut depth

    // Name the resulting part for the BOM / browser.
    setProperty(context, {
            "entities" : qCreatedBy(id + "body", EntityType.BODY),
            "propertyType" : PropertyType.NAME,
            "value" : "MotorProxy"
    });
}

// ----------------------------------------------------------------------------
//  Build ONE ring of bolt holes in a target body, by:
//   1) sketching a seed circle at the bolt-circle radius on the face plane,
//   2) extruding it as a NEW solid tool body (the "drill"),
//   3) circular-patterning the tool body around the axis, then
//   4) boolean-subtracting all tool bodies from the target body.
//
//  Using NEW tool bodies (instead of a direct REMOVE extrude) is what makes
//  the circular pattern robust: opPattern needs a real body to copy, and a
//  REMOVE extrude leaves no body behind to query.
// ----------------------------------------------------------------------------
function makeBoltRing(context is Context, id is Id, targetBodyId is Id,
                      cSys is CoordSystem, bcRadius is ValueWithUnits,
                      nBolts is number, holeRadius is ValueWithUnits,
                      faceZ is ValueWithUnits, cutDir is Vector,
                      cutDepth is ValueWithUnits)
{
    if (nBolts < 1)
    {
        return;
    }

    // Face plane: origin offset along the body axis to the face, normal = axis.
    const faceOrigin = cSys.origin + cSys.zAxis * faceZ;
    const facePlane  = plane(faceOrigin, cSys.zAxis, cSys.xAxis);

    // 1) Seed circle, placed on the +X spoke of the bolt circle (sketch coords).
    const sketchId = id + "sketch";
    var sk = newSketchOnPlane(context, sketchId, { "sketchPlane" : facePlane });
    skCircle(sk, "seed", {
            "center" : vector(bcRadius, 0 * meter),
            "radius" : holeRadius
    });
    skSolve(sk);

    // 2) Extrude the seed as a NEW solid tool body into the part.
    opExtrude(context, id + "drill", {
            "entities"      : qSketchRegion(sketchId),
            "direction"     : cutDir,
            "endBound"      : BoundingType.BLIND,
            "endDepth"      : cutDepth,
            "operationType" : NewBodyOperationType.NEW
    });

    // 3) Circular-pattern the tool body around the body axis (n-1 copies).
    if (nBolts > 1)
    {
        const axisLine = line(cSys.origin, cSys.zAxis);
        var transforms = [];
        var names = [];
        for (var i = 1; i < nBolts; i += 1)
        {
            transforms = append(transforms,
                    rotationAround(axisLine, (i * 360 / nBolts) * degree));
            names = append(names, "bolt" ~ toString(i));
        }
        opPattern(context, id + "pattern", {
                "entities"      : qCreatedBy(id + "drill", EntityType.BODY),
                "transforms"    : transforms,
                "instanceNames" : names
        });
    }

    // 4) Subtract the drill seed + all its pattern copies from the target body.
    //    (If nBolts == 1, the "pattern" query is simply empty and is ignored.)
    opBoolean(context, id + "subtract", {
            "operationType" : BooleanOperationType.SUBTRACTION,
            "targets"       : qCreatedBy(targetBodyId, EntityType.BODY),
            "tools"         : qUnion([qCreatedBy(id + "drill", EntityType.BODY),
                                      qCreatedBy(id + "pattern", EntityType.BODY)])
    });
}