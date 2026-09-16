// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature11Presentation",
    products: [.library(name: "Feature11Presentation", targets: ["Feature11Presentation"])],
    dependencies: [.package(path: "../Feature11Domain"),
        .package(path: "../Feature11Data")],
    targets: [.target(name: "Feature11Presentation", dependencies: [.product(name: "Feature11Domain", package: "Feature11Domain"), .product(name: "Feature11Data", package: "Feature11Data")])]
)
