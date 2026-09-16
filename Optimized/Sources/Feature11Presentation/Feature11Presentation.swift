import Feature11Domain
import Feature11Data

public enum Feature11PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature11DomainModel = Feature11DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
