// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature05Presentation",
    products: [.library(name: "Feature05Presentation", targets: ["Feature05Presentation"])],
    dependencies: [.package(path: "../Feature05Domain"),
        .package(path: "../Feature05Data")],
    targets: [.target(name: "Feature05Presentation", dependencies: [.product(name: "Feature05Domain", package: "Feature05Domain"), .product(name: "Feature05Data", package: "Feature05Data")])]
)
