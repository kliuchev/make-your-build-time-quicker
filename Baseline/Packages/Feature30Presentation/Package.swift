// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature30Presentation",
    products: [.library(name: "Feature30Presentation", targets: ["Feature30Presentation"])],
    dependencies: [.package(path: "../Feature30Domain"),
        .package(path: "../Feature30Data")],
    targets: [.target(name: "Feature30Presentation", dependencies: [.product(name: "Feature30Domain", package: "Feature30Domain"), .product(name: "Feature30Data", package: "Feature30Data")])]
)
