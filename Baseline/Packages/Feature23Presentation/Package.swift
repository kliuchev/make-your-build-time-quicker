// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature23Presentation",
    products: [.library(name: "Feature23Presentation", targets: ["Feature23Presentation"])],
    dependencies: [.package(path: "../Feature23Domain"),
        .package(path: "../Feature23Data")],
    targets: [.target(name: "Feature23Presentation", dependencies: [.product(name: "Feature23Domain", package: "Feature23Domain"), .product(name: "Feature23Data", package: "Feature23Data")])]
)
